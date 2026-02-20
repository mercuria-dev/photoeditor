import asyncio
import html
from PIL import Image
import config
from modules.lang import get_translation, get_translation_parsed
import shutil
from datetime import datetime, timezone, timedelta
import os

from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from modules import database
from modules.states import GenAIState, IllusionAIState, EditState, SpamState, AddUpText, AddDownText, CutAIState
from modules.keyboards import ban_kb, link_kb, func_kb, ai_kb, edit_kb, ai_continue, admin_kb, font_kb
from modules.callback_data import Ban, AddText
from modules.middleware import ExistsUserMiddleware
from func.editor import liquid_rescale, bad_quality, make_sketch, make_moire, add_text_to_photo, \
    make_noise, make_bright, make_sat


# start
async def welcome(message: Message):
    start_msg, start_entities = get_translation_parsed("start_msg", message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile("photo.jpg"),
        caption=start_msg,
        caption_entities=start_entities,
        parse_mode=None,
        reply_markup=func_kb(message.from_user.id),
    )

# editor
async def edit(message: Message, state: FSMContext):
    msg, entities = get_translation_parsed("send_to_edit", message.from_user.id)
    await message.answer(msg, entities=entities, parse_mode=None)
    await state.set_state(EditState.get_photo)

async def edit_call(call: CallbackQuery, state: FSMContext):
    await call.answer()
    msg, entities = get_translation_parsed("send_to_edit", call.from_user.id)
    await call.message.answer(msg, entities=entities, parse_mode=None)
    await state.set_state(EditState.get_photo)

async def photo(message: Message, state: FSMContext):
    await state.clear()
    photo_link = f"photos/{message.from_user.id}.jpg"
    if message.photo:
        file_id = await download_photo(message, message.from_user.id)
        await message.bot.send_photo(chat_id=config.LOG_CHAT, photo=file_id, caption=f"<code>{message.from_user.id}</code> <a href='{message.from_user.url}'>{message.from_user.first_name}</a> sended", parse_mode="html", reply_markup=ban_kb(message.from_user.id))
        im = Image.open(photo_link)
        width, height = im.size
        while width > 800:
            width = (width//4)*3
            height = (height//4)*3
        while height > 800:
            width = (width//4)*3
            height = (height//4)*3
        im = im.resize((width, height))
        im.save(photo_link)
        msg, msg_entities = get_translation_parsed("menu", message.from_user.id)
        await message.answer_photo(
            photo=FSInputFile(photo_link),
            caption=msg,
            caption_entities=msg_entities,
            parse_mode=None,
            reply_markup=edit_kb(message.from_user.id),
        )

async def jm(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await liquid_rescale(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def call_bad_quality(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await bad_quality(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def sketch(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await make_sketch(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def moire(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await make_moire(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def noise(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await make_noise(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def bright(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await make_bright(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def sat(call: CallbackQuery):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    photo_link = f"photos/{call.from_user.id}.jpg"
    await make_sat(photo_link)
    msg, msg_entities = get_translation_parsed("result", call.from_user.id)
    await call.message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(call.from_user.id),
    )

async def choose_font(call: CallbackQuery):
    await call.answer()
    msg, msg_entities = get_translation_parsed("choose_font", call.from_user.id)
    file_id = await download_photo(call.message, call.from_user.id)
    await call.message.answer_photo(
        photo=file_id,
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=font_kb(),
    )

async def add_text(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    await download_photo(call.message, call.from_user.id)
    await state.update_data(font=callback_data.font)
    msg, msg_entities = get_translation_parsed("add_up_text", call.from_user.id)
    await call.message.answer(msg, entities=msg_entities, parse_mode=None)
    await state.set_state(AddUpText.text)

async def add_up_text(message: Message, state: FSMContext):
    if message.text == "/skip":
        up_text = ""
    else:
        up_text = message.text
    await state.update_data(up_text=up_text)
    msg, msg_entities = get_translation_parsed("add_down_text", message.from_user.id)
    await message.answer(msg, entities=msg_entities, parse_mode=None)
    await state.set_state(AddDownText.text)

async def add_down_text(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    font = data["font"]
    up_text = data["up_text"]
    if message.text == "/skip":
        down_text = ""
    else:
        down_text = message.text
    photo_link = f"photos/{message.from_user.id}.jpg"
    await add_text_to_photo(font, up_text, down_text, photo_link)
    msg, msg_entities = get_translation_parsed("result", message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile(photo_link),
        caption=msg,
        caption_entities=msg_entities,
        parse_mode=None,
        reply_markup=edit_kb(message.from_user.id),
    )

# other func

async def donate(call: CallbackQuery):
    await call.answer()
    file_id = await download_photo(call.message, call.from_user.id)
    msg, _msg_entities = get_translation_parsed("donate", call.from_user.id)
    donate_text = f"🖤{msg}:\n"

    cryptobot_url = config.CRYPTOBOT_INVOICE_URL
    if cryptobot_url:
        cryptobot_url = html.escape(cryptobot_url, quote=True)
        donate_text += f"Crypto Bot <a href=\"{cryptobot_url}\">send</a>"
    else:
        donate_text += "Crypto Bot: <code>CRYPTOBOT_INVOICE_URL</code> is not set"
    p = InputMediaPhoto(media=file_id, caption=donate_text, parse_mode='html')
    await call.message.edit_media(media=p, reply_markup=func_kb(call.from_user.id), disable_web_page_preview=True)

async def check_sub(call: CallbackQuery):
    await call.answer()
    try:
        member = await call.bot.get_chat_member(chat_id=config.CHANNEL, user_id=call.from_user.id)
        # statuses: 'creator', 'administrator', 'member', 'restricted', 'left', 'kicked'
        if member.status in ('creator', 'administrator', 'member'):
            msg, msg_entities = get_translation_parsed("subscribed", call.from_user.id)
        else:
            msg, msg_entities = get_translation_parsed("not_subscribed", call.from_user.id)
    except Exception:
        # if any error (for example bot not in channel or invalid channel id) treat as not subscribed
        msg, msg_entities = get_translation_parsed("not_subscribed", call.from_user.id)
    await call.message.answer(msg, entities=msg_entities, parse_mode=None)

async def download_photo(message, user_id):
    photo_link = f"photos/{user_id}.jpg"
    file_info = await message.bot.get_file(message.photo[-1].file_id)
    downloaded_file = await message.bot.download_file(file_info.file_path)
    with open(photo_link, 'wb') as new_file:
        new_file.write(downloaded_file.getvalue())
    return message.photo[-1].file_id

async def lang(call: CallbackQuery):
    language = database.select(f"select locale from users where id = {call.from_user.id}", one=True)[0]
    if language == "en":
        database.insert_delete(f"update users set locale = 'ru' where id = {call.from_user.id}")
        await call.answer("🇷🇺Ваш язык изменён на русский")
    else:
        database.insert_delete(f"update users set locale = 'en' where id = {call.from_user.id}")
        await call.answer("🇺🇸Your language is english")

# admin
async def ban(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    user_id = callback_data.id
    await call.bot.ban_chat_member(chat_id=config.CHANNEL, user_id=user_id)
    await call.message.answer(f"❌<code>{user_id}</code> blocked", parse_mode='html')

async def admin(call: CallbackQuery):
    await call.answer()
    if str(call.from_user.id) in config.ADMIN_IDS:
        await call.message.answer("⚠️Выберите, что нужно делать", reply_markup=admin_kb())

async def spam(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("💚Отправьте сообщение\n❌/cansel")
    await state.set_state(SpamState.start)

async def send_spam(message: Message, state: FSMContext):
    await state.clear()
    if message.text == "/cansel":
        await message.answer("❌Отменено!")
        return
    await message.answer("🚀Запущено")
    users = database.select(f"select id from users")
    keyboard = None
    txt = message.html_text
    if message.reply_markup:
        keyboard = message.reply_markup
    if message.photo:
        file_id = message.photo[-1].file_id
        for user in users:
            try:
                await message.bot.send_photo(
                    chat_id=user[0],
                    caption=txt,
                    photo=file_id,
                    parse_mode="html",
                    reply_markup=keyboard
                )
            except:
                pass
    if message.sticker:
        file_id = message.sticker.file_id
        for user in users:
            try:
                await message.bot.send_sticker(
                    chat_id=user[0],
                    sticker=file_id
                )
            except:
                pass
    elif message.video:
        file_id = message.video.file_id
        for user in users:
            try:
                await message.bot.send_video(
                    chat_id=user[0],
                    caption=txt,
                    video=file_id,
                    parse_mode="html",
                    reply_markup=keyboard
                )
            except:
                pass
    elif message.animation:
        file_id = message.animation.file_id
        for user in users:
            try:
                await message.bot.send_animation(
                    chat_id=user[0],
                    caption=txt,
                    animation=file_id,
                    parse_mode="html",
                    reply_markup=keyboard
                )
            except:
                pass
    if message.text:
        for user in users:
            try:
                await message.bot.send_message(
                    chat_id=user[0],
                    text=txt,
                    parse_mode="html",
                    reply_markup=keyboard
                )
            except:
                pass
    await message.answer("✅Finished")

async def send_db(bot):
    msk_tz = timezone(timedelta(hours=3))
    now = datetime.now(msk_tz)
    filename = f"db_{now.strftime('%Y-%m-%d_%H-%M')}_MSK.db"
    shutil.copy("base/db.db", filename)
    await bot.send_document(chat_id=config.LOG_CHAT, document=FSInputFile(filename), caption=f"Database backup: {filename}")
    os.remove(filename)

async def scheduler(bot):
    while True:
        await send_db(bot)
        await asyncio.sleep(10800)  # 3 hours in seconds

async def main():
    bot_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=config.API_TOKEN, default=bot_properties)
    dp = Dispatcher(storage=MemoryStorage())
    # middleware
    dp.message.middleware(ExistsUserMiddleware())
    # start
    dp.message.register(welcome, Command(commands="start"))
    dp.callback_query.register(lang, F.data == "lang")
    # admin
    dp.callback_query.register(admin, F.data == "admin")
    dp.callback_query.register(spam, F.data == "spam")
    dp.message.register(send_spam, SpamState.start)
    # edit
    dp.message.register(edit, Command(commands="edit"))
    dp.callback_query.register(edit_call, F.data == "edit")
    dp.callback_query.register(call_bad_quality, F.data == "bad_quality")
    dp.callback_query.register(jm, F.data == "jm")
    dp.callback_query.register(sketch, F.data == "sketch")
    dp.callback_query.register(moire, F.data == "moire")

    dp.callback_query.register(noise, F.data == "noise")
    dp.callback_query.register(bright, F.data == "bright")
    dp.callback_query.register(sat, F.data == "sat")

    dp.message.register(photo, EditState.get_photo)
    dp.callback_query.register(choose_font, F.data == "text")
    dp.callback_query.register(add_text, AddText.filter())
    dp.message.register(add_up_text, AddUpText.text)
    dp.message.register(add_down_text, AddDownText.text)
    # other commands
    dp.callback_query.register(donate, F.data == "donate")
    dp.callback_query.register(check_sub, F.data == "check_sub")
    dp.callback_query.register(ban, Ban.filter())
    print("Bot started")
    asyncio.create_task(scheduler(bot))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
