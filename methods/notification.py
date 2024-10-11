from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import set_msg_id
from utils.wrap_db import db
from utils.wrap_cache import cache



class NotificationManager:

    @cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cache_db, edit=True):
        """
            manager requests this methods 
        """
        
        query = update.callback_query
        callback_pointer = {
            'notif_click': lambda: self.click(update, context, cache_db),
        }

        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()


    async def click(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cache_db):
        
        chat_id = update.effective_chat.id
        query = update.callback_query

        try:
            await query.message.delete()
        
        except:
            inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support)
                    ]
                ])
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_delete_msg, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, cache_db)
            return 
