from telegram.ext import ContextTypes
from db.db_user import get_all_users
from utils.wrap_cache import cache
from utils.wrap_db import db
from lang import loadStrings
from telegram import Update
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from cache.cache_session import (
    get_position,
    delete_cache,
    set_msg_id,
    set_position,
    get_session
)

# from api.profile import get_profile

class MenuManager:

    @db
    @cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, cache_db, edit= False):
        """
            manager requests this methods 
        """

        chat_id = update.effective_chat.id

        position = get_position(chat_id, cache_db)

        message_pointer = {
            'mainmenu': lambda: self.mainmenu(update, context, db, cache_db, edit)
        }

        callback_pointer = {
            'mainmenu': lambda: self.mainmenu(update, context, db, cache_db, edit)
        }

        if edit: 
            
            query = update.callback_query

            if query.data.split('_')[0] in  callback_pointer:
                await callback_pointer[query.data.split('_')[0]]()

        else:
            if position in message_pointer:
                await message_pointer[position]()

    async def mainmenu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, cache_db, edit= False):
        """
            show main menu
        """
        chat_id = update.effective_chat.id
        delete_cache(chat_id, db)

        set_position(chat_id, 'mainmenu', db)

        inline_options = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(loadStrings.callback_text.user_manager, callback_data= 'usermanager'),
            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.message_manager, callback_data= 'messagemanager')

            ],
            [
                InlineKeyboardButton(loadStrings.callback_text.support, callback_data= 'support')
            ]
        ])

        users = get_all_users(db)

        active_users_numbers = len([user for user in users if user.status == True])
        users_number = len(users)
        inactive_users_number = users_number - active_users_numbers

        text = loadStrings.text.menu.format(username, total_user, enable_ssh_services, disable_ssh_services, deleted_ssh_services, balance)
        if edit: 
            resp_msg = await update.callback_query.edit_message_text( text, reply_markup= inline_options)
        
        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= text, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)