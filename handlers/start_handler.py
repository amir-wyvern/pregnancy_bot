
from cache.cache_session import set_position, set_msg_id
from utils.msg_delete import msg_delete_all
from utils.wrap_auth import auth
from utils.wrap_db import db
from utils.wrap_cache import cache

from telegram.ext import ContextTypes
from methods.menu import MenuManager
from telegram import Update

@db
@cache
@auth
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, db, cache_db ):

    chat_id = update.effective_chat.id 

    set_position(chat_id, 'mainmenu', db)
    await msg_delete_all(chat_id, db)

    set_msg_id(chat_id, update.message.message_id, db)
    await MenuManager().manager(update, context)

