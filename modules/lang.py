from modules import database
import json
from html.parser import HTMLParser

from aiogram.enums import MessageEntityType
from aiogram.types import MessageEntity
from aiogram.utils.text_decorations import add_surrogates


def _utf16_len(text: str) -> int:
    # Telegram entity offsets/lengths are in UTF-16 code units
    return len(add_surrogates(text)) // 2


class _TelegramHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.entities: list[MessageEntity] = []
        self._offset: int = 0  # UTF-16 code units
        self._stack: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k: v for k, v in attrs}

        if tag == "a":
            href = attrs_dict.get("href")
            if href:
                self._stack.append({"tag": "a", "start": self._offset, "href": href})
            return

        if tag == "tg-emoji":
            emoji_id = attrs_dict.get("emoji-id") or attrs_dict.get("emoji_id")
            if emoji_id:
                self._stack.append({"tag": "tg-emoji", "start": self._offset, "emoji_id": emoji_id})
            return

    def handle_endtag(self, tag: str) -> None:
        # Pop the nearest matching tag frame (handles malformed nesting gracefully)
        for i in range(len(self._stack) - 1, -1, -1):
            frame = self._stack[i]
            if frame.get("tag") != tag:
                continue
            self._stack.pop(i)
            start = int(frame["start"])
            length = self._offset - start
            if length <= 0:
                return

            if tag == "a":
                href = frame.get("href")
                if href:
                    self.entities.append(
                        MessageEntity(
                            type=MessageEntityType.TEXT_LINK,
                            offset=start,
                            length=length,
                            url=href,
                        )
                    )
                return

            if tag == "tg-emoji":
                emoji_id = frame.get("emoji_id")
                if emoji_id:
                    self.entities.append(
                        MessageEntity(
                            type=MessageEntityType.CUSTOM_EMOJI,
                            offset=start,
                            length=length,
                            custom_emoji_id=str(emoji_id),
                        )
                    )
                return

    def handle_data(self, data: str) -> None:
        if not data:
            return
        self.parts.append(data)
        self._offset += _utf16_len(data)


def parse_telegram_html(value: str) -> tuple[str, list[MessageEntity]]:
    """Parse a limited Telegram-flavored HTML subset into (text, entities).

    Supports:
    - <tg-emoji emoji-id="...">X</tg-emoji> -> CUSTOM_EMOJI entity
    - <a href="...">text</a> -> TEXT_LINK entity

    Other tags are ignored (their inner text is preserved).
    """
    parser = _TelegramHtmlParser()
    parser.feed(value or "")
    text = "".join(parser.parts)
    # Entities must be sorted by offset
    entities = sorted(parser.entities, key=lambda e: e.offset)
    return text, entities


def get_translation_parsed(key: str, user_id: int) -> tuple[str, list[MessageEntity]]:
    raw = get_translation(key, user_id)
    return parse_telegram_html(raw)


def get_translation_plain(key: str, user_id: int) -> str:
    text, _entities = get_translation_parsed(key, user_id)
    return text


class _TelegramButtonHtmlParser(HTMLParser):
    """Parse a Telegram HTML-ish button label.

    For buttons we can't send entities, but we can set `icon_custom_emoji_id`.
    We take the first <tg-emoji emoji-id="...">...</tg-emoji> and convert it to icon.
    The inner emoji glyph for that first tag is not included in output text to avoid duplication.
    Other tags are ignored, their inner text is preserved.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.icon_custom_emoji_id: str | None = None
        self._in_tg_emoji_depth = 0
        self._current_tg_emoji_is_icon = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "tg-emoji":
            return
        attrs_dict = {k: v for k, v in attrs}
        emoji_id = attrs_dict.get("emoji-id") or attrs_dict.get("emoji_id")

        self._in_tg_emoji_depth += 1

        if self.icon_custom_emoji_id is None and emoji_id:
            self.icon_custom_emoji_id = str(emoji_id)
            self._current_tg_emoji_is_icon = True
        else:
            self._current_tg_emoji_is_icon = False

    def handle_endtag(self, tag: str) -> None:
        if tag != "tg-emoji":
            return
        if self._in_tg_emoji_depth > 0:
            self._in_tg_emoji_depth -= 1
        if self._in_tg_emoji_depth == 0:
            self._current_tg_emoji_is_icon = False

    def handle_data(self, data: str) -> None:
        if not data:
            return
        # If this tg-emoji was used as icon, don't duplicate its glyph in text
        if self._in_tg_emoji_depth > 0 and self._current_tg_emoji_is_icon:
            return
        self.parts.append(data)


def parse_telegram_button_html(value: str) -> tuple[str, str | None]:
    parser = _TelegramButtonHtmlParser()
    parser.feed(value or "")
    text = "".join(parser.parts).strip()
    return text, parser.icon_custom_emoji_id


def get_translation_button(key: str, user_id: int) -> tuple[str, str | None]:
    raw = get_translation(key, user_id)
    return parse_telegram_button_html(raw)

def get_translation(key, user_id):
    language = database.select(f"select locale from users where id = {user_id}", one=True)[0]
    with open(f'lang/{language}.json', 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations.get(key, '')

