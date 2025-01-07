from aiogram.utils.keyboard import InlineKeyboardBuilder
import config
from modules.callback_data import Ban, AddText
from modules.lang import get_translation


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
    text = get_translation("sub_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=text, url=config.CHANNEL_LINK)
    kb.adjust(1)
    return kb.as_markup()

def func_kb(user_id):
    donate_btn = get_translation("donate_btn", user_id)
    edit_btn = get_translation("edit_btn", user_id)
    lang_btn = get_translation("lang_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=edit_btn, callback_data="edit")
    kb.button(text=donate_btn, callback_data="donate")
    kb.button(text=lang_btn, callback_data="lang")
    if str(user_id) in config.ADMIN_IDS:
        kb.button(text="⚡️Admin", callback_data="admin")
    kb.adjust(1, 3)
    return kb.as_markup()

def ai_kb(user_id):
    generator_ai_btn = get_translation("generator_ai_btn", user_id)
    illusion_ai_btn = get_translation("illusion_ai_btn", user_id)
    cut_ai_btn = get_translation("cut_ai_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=generator_ai_btn, callback_data="gen")
    kb.button(text=illusion_ai_btn, callback_data="illusion")
    kb.button(text=cut_ai_btn, callback_data="cutter")
    kb.adjust(2)
    return kb.as_markup()

def ai_continue(ai_type, user_id):
    new_ai_request = get_translation("new_ai_request", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=new_ai_request, callback_data=ai_type)
    kb.adjust(1)
    return kb.as_markup()

def edit_kb(user_id):
    rescale_btn = get_translation("rescale_btn", user_id)
    bad_btn = get_translation("bad_btn", user_id)
    sketch_btn = get_translation("sketch_btn", user_id)
    moire_btn = get_translation("moire_btn", user_id)

    noice_btn = get_translation("noise_btn", user_id)
    bright_btn = get_translation("bright_btn", user_id)
    sat_btn = get_translation("sat_btn", user_id)

    new_edit_btn = get_translation("new_edit_btn", user_id)
    text_btn = get_translation("text_btn", user_id)
    kb = InlineKeyboardBuilder()
    kb.button(text=rescale_btn, callback_data="jm")
    kb.button(text=bad_btn, callback_data="bad_quality")
    kb.button(text=sketch_btn, callback_data="sketch")
    kb.button(text=moire_btn, callback_data="moire")

    kb.button(text=noice_btn, callback_data="noise")
    kb.button(text=bright_btn, callback_data="bright")
    kb.button(text=sat_btn, callback_data="sat")

    kb.button(text=text_btn, callback_data="text")
    kb.button(text=new_edit_btn, callback_data="edit")
    kb.adjust(2, 2, 3, 1, 1)
    return kb.as_markup()

def font_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="Gothic", callback_data=AddText(font="goth"))
    kb.button(text="Impact", callback_data=AddText(font="impact"))
    kb.adjust(2)
    return kb.as_markup()
