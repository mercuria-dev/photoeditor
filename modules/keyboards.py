from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from modules.callback_data import Ban, AddText
from modules.lang import get_translation_button


def ban_kb(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="❌Ban", callback_data=Ban(id=user_id))
    kb.adjust(1)
    return kb.as_markup()

def admin_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="📬Send message to user", callback_data="spam")
    kb.adjust(1)
    return kb.as_markup()

def link_kb(user_id):
    text, text_icon = get_translation_button("sub_btn", user_id)
    check_btn, check_icon = get_translation_button("check_sub_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=text, url=config.CHANNEL_LINK, icon_custom_emoji_id=text_icon)
    kb.button(text=check_btn, callback_data="check_sub", icon_custom_emoji_id=check_icon)
    # first row - link, second row - check subscription
    kb.adjust(1, 1)
    return kb.as_markup()

def func_kb(user_id):
    donate_btn, donate_icon = get_translation_button("donate_btn", user_id)
    edit_btn, edit_icon = get_translation_button("edit_btn", user_id)
    lang_btn, lang_icon = get_translation_button("lang_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=edit_btn, callback_data="edit", icon_custom_emoji_id=edit_icon)
    kb.button(text=donate_btn, callback_data="donate", icon_custom_emoji_id=donate_icon)
    kb.button(text=lang_btn, callback_data="lang", icon_custom_emoji_id=lang_icon)
    if str(user_id) in config.ADMIN_IDS:
        kb.button(text="Admin", callback_data="admin", icon_custom_emoji_id="5431449001532594346")
    kb.adjust(1, 3)
    return kb.as_markup()

def ai_kb(user_id):
    generator_ai_btn, gen_icon = get_translation_button("generator_ai_btn", user_id)
    illusion_ai_btn, ill_icon = get_translation_button("illusion_ai_btn", user_id)
    cut_ai_btn, cut_icon = get_translation_button("cut_ai_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=generator_ai_btn, callback_data="gen", icon_custom_emoji_id=gen_icon)
    kb.button(text=illusion_ai_btn, callback_data="illusion", icon_custom_emoji_id=ill_icon)
    kb.button(text=cut_ai_btn, callback_data="cutter", icon_custom_emoji_id=cut_icon)
    kb.adjust(2)
    return kb.as_markup()

def ai_continue(ai_type, user_id):
    new_ai_request, new_icon = get_translation_button("new_ai_request", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=new_ai_request, callback_data=ai_type, icon_custom_emoji_id=new_icon)
    kb.adjust(1)
    return kb.as_markup()

def edit_kb(user_id):
    rescale_btn, rescale_icon = get_translation_button("rescale_btn", user_id)
    bad_btn, bad_icon = get_translation_button("bad_btn", user_id)
    sketch_btn, sketch_icon = get_translation_button("sketch_btn", user_id)
    moire_btn, moire_icon = get_translation_button("moire_btn", user_id)

    noice_btn, noise_icon = get_translation_button("noise_btn", user_id)
    bright_btn, bright_icon = get_translation_button("bright_btn", user_id)
    sat_btn, sat_icon = get_translation_button("sat_btn", user_id)

    new_edit_btn, new_edit_icon = get_translation_button("new_edit_btn", user_id)
    text_btn, text_icon = get_translation_button("text_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=rescale_btn, callback_data="jm", icon_custom_emoji_id=rescale_icon)
    kb.button(text=bad_btn, callback_data="bad_quality", icon_custom_emoji_id=bad_icon)
    kb.button(text=sketch_btn, callback_data="sketch", icon_custom_emoji_id=sketch_icon)
    kb.button(text=moire_btn, callback_data="moire", icon_custom_emoji_id=moire_icon)

    kb.button(text=noice_btn, callback_data="noise", icon_custom_emoji_id=noise_icon)
    kb.button(text=bright_btn, callback_data="bright", icon_custom_emoji_id=bright_icon)
    kb.button(text=sat_btn, callback_data="sat", icon_custom_emoji_id=sat_icon)

    kb.button(text=text_btn, callback_data="text", icon_custom_emoji_id=text_icon)
    kb.button(text=new_edit_btn, callback_data="edit", icon_custom_emoji_id=new_edit_icon)
    kb.adjust(2, 2, 3, 1, 1)
    return kb.as_markup()

def font_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Gothic", callback_data=AddText(font="goth"))
    kb.button(text="Impact", callback_data=AddText(font="impact"))
    kb.adjust(2)
    return kb.as_markup()
