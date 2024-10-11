from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from db.db_admin import get_admin_by_username
from utils.msg_delete import msg_delete_all
from passlib.context import CryptContext
from telegram.ext import ContextTypes
from methods.menu import MenuManager
from utils.wrap_cache import cache
from utils.wrap_db import db
from lang import loadStrings
from telegram import Update
from cache.cache_session import (
    set_position,
    get_position,
    delete_cache,
    set_cache,
    get_cache,
    set_session,
    set_msg_id
)
import logging


logger = logging.getLogger('login_method.log') 
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('login_method.log') 
file_handler.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s') 
file_handler.setFormatter(formatter) 
logger.addHandler(file_handler) 

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class LoginManager:

    @db
    @cache
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, cache_db, edit=False):
        """
            manager requests this methods 
        """
        chat_id = update.effective_chat.id
        
        query = update.callback_query

        self.callback_pointer = {
            'login_edit_username': lambda : self.login_username(update, context, cache_db, edit= edit),
            'login_edit_password': lambda : self.login_password(update, context, cache_db, edit= edit)
        }


        self.message_pointer = {
            'login_manager': lambda: self.login_username(update, context, cache_db),
            'login_get_username': lambda: self.login_get_username(update, context, cache_db),
            'login_password': lambda: self.login_password(update, context, cache_db),
            'login_get_password': lambda: self.login_get_password(update, context, db, cache_db),
            'login_api': lambda: self.login_api(update, context, db, cache_db)
        }
        
        if edit :

            if query.data in self.callback_pointer: 
                await self.callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)

            print('login pos:', pos)
            
            if pos in self.message_pointer :
                await self.message_pointer[pos]()


    async def login_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cache_db, edit= False):
        """
            send message for get username
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_get_username', cache_db)

        if edit:
            query = update.callback_query
            await query.edit_message_text(text= loadStrings.text.login_username)
        
        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_username)
            set_msg_id(chat_id, resp_msg.message_id, cache_db)

    async def login_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cache_db):
        """
            get username
        """
        chat_id = update.effective_chat.id
        cache = { 'username':  update.message.text}

        set_cache(chat_id, cache, db)

        await self.login_password(update, context, db)

    async def login_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, cache_db, edit= False):
        """
            send message for get password
        """
        chat_id = update.effective_chat.id
        set_position(chat_id, 'login_get_password', db)

        inline_options = InlineKeyboardMarkup([
            [   
                InlineKeyboardButton(loadStrings.callback_text.login_edit_username, callback_data= 'login_edit_username'),
            ]
        ])
        
        if edit:
            
            query = update.callback_query
            await query.edit_message_text(text= loadStrings.text.login_password, reply_markup= inline_options)

        else:
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_password, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)

    async def login_get_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, cache_db):
        """
            get password
        """

        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, cache_db)
        cache['password'] = update.message.text

        set_cache(chat_id, cache, cache_db)

        set_position(chat_id, 'None', cache_db)

        await self.login_api(update, context, db)

    async def login_api(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        """
            send request to api and get the session
        """
        chat_id = update.effective_chat.id
        cache = get_cache(chat_id, db)

        resp = get_admin_by_username(cache['username'], db)
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if not resp or not pwd_context.verify(cache['password'], resp.password):
            options = InlineKeyboardMarkup([[
                InlineKeyboardButton(loadStrings.button.edit_password, callback_data='login_edit_password')
                ]])

            resp_msg = await  context.bot.send_message(chat_id= chat_id, text= loadStrings.text.login_failed, reply_markup=options)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return 
                        

        delete_cache(chat_id, db)
        await msg_delete_all(chat_id, db)
        
        set_session(chat_id, True, db)

        resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.inital_msg)

        username = cache['username']
        logger.info(f'login msg_id [username: {username} -msg_id: {resp_msg.message_id}]')

        # link to main menu
        await MenuManager().manager(update, context)

