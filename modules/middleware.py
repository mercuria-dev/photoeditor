# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware
from modules import database
from modules.keyboards import ban_kb, link_kb
from modules.lang import get_translation_parsed
import config


class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user = event.from_user
        chat_exist = database.select(f"select * from users where id = {user.id}")
        if not chat_exist:
            database.insert_delete(f"insert into users (id) values ({user.id})")
            await event.bot.send_message(chat_id=config.LOG_CHAT, text=f"New user <code>{user.id}</code> <a href='{user.url}'>{user.first_name}</a>", parse_mode="html", reply_markup=ban_kb(user.id))
        user_status = await event.bot.get_chat_member(chat_id=config.CHANNEL, user_id=user.id)
        if user_status.status == "kicked":
            return
        if user_status.status != "left":
            return await handler(event, data)
        else:
            msg, msg_entities = get_translation_parsed("sub_msg", user.id)
            await event.bot.send_message(
                chat_id=user.id,
                text=msg,
                entities=msg_entities,
                parse_mode=None,
                reply_markup=link_kb(user.id)
            )
            return
