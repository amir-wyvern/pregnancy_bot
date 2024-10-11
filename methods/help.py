from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from utils.wrap_db import db_cache
from utils.wrap_auth import auth

class HelpManager:

    @db_cache
    @auth
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'help': lambda: self.help(update, context, db),
        }

        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        query = update.callback_query

        inline_options = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')]
                ]
            )

        await query.edit_message_text( loadStrings.text.manageusers_help, reply_markup= inline_options, parse_mode='markdown')
        
        