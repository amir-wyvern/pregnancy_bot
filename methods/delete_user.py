from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes
from telegram import Update
from lang import loadStrings
from cache.cache_session import (
    set_position,
    get_position,
    get_session,
    set_msg_id
)
from utils.wrap_cache import cache
from utils.wrap_auth import auth
# from api.services import delete_user_ssh_service
from methods.manage_users import ManageUsersManager

class DeleteUserManager:

    @cache
    @auth
    async def manager(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db, edit=True):
        """
            manager requests this methods 
        """

        query = update.callback_query
        callback_pointer = {
            'deleteuser': lambda: self.delete_user(update, context, db),
        }

        message_pointer = {
            'deleteuser_get_username': lambda: self.delete_user_get_username(update, context, db)
        }
        
        if edit :

            if query.data in callback_pointer: 
                await callback_pointer[query.data]()

        else:

            chat_id = update.effective_chat.id
            pos = get_position(chat_id, db)
            
            if pos in message_pointer :
                await message_pointer[pos]()

    async def delete_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id
        query = update.callback_query

        set_position(chat_id, 'deleteuser_get_username', db) 

        try:
            await query.message.delete()

        except:
            inline_options = InlineKeyboardMarkup([
                    [   
                        InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support)
                    ]
                ])
            resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.error_delete_msg, reply_markup= inline_options)
            set_msg_id(chat_id, resp_msg.message_id, db)
            return 
        
        inline_options = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'manageusers')]
                ]
            )

        resp_msg =  await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.delete_config_text, reply_markup= inline_options)
        set_msg_id(chat_id, resp_msg.message_id, db)

    async def delete_user_get_username(self, update: Update, context: ContextTypes.DEFAULT_TYPE, db):
        
        chat_id = update.effective_chat.id

        text = update.message.text
        session = get_session(chat_id, db)
        
        # resp = delete_user_ssh_service(session, text)
        
        # if resp.status_code != 200:
            
        #     if resp.status_code in [404, 409, 400]:

        #         message = loadStrings.text.internal_error

        #         if resp.json()['detail']['internal_code'] == 2433:
        #             message = loadStrings.text.error_username_not_have_service

        #         elif resp.json()['detail']['internal_code'] == 2437:
        #             message = loadStrings.text.error_service_deleted

        #         elif resp.json()['detail']['internal_code'] == 2419:
        #             message = loadStrings.text.error_not_agent

        #         elif resp.json()['detail']['internal_code'] == 2415:
        #             message = loadStrings.text.error_already_block
                
        #         inline_options = InlineKeyboardMarkup([
        #             [   
        #                 InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
        #                 InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'blockuser')
        #             ]
        #         ])

        #         resp_msg = await context.bot.send_message(chat_id= chat_id, text= message, reply_markup= inline_options)
        #         set_msg_id(chat_id, resp_msg.message_id, db)
                
        #         return

        #     else:
        
        #         inline_options = InlineKeyboardMarkup([
        #             [   
        #                 InlineKeyboardButton(loadStrings.callback_text.support, url= loadStrings.callback_url.support),
        #                 InlineKeyboardButton(loadStrings.callback_text.back, callback_data= 'deleteuser')
        #             ]
        #         ])

        #         resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.internal_error, reply_markup= inline_options)
        #         set_msg_id(chat_id, resp_msg.message_id, db)
        #         return

        # resp_msg = await context.bot.send_message(chat_id= chat_id, text= loadStrings.text.delete_user_success.format(text), parse_mode='markdown')
        # set_msg_id(chat_id, resp_msg.message_id, db)
        
        # set_position(chat_id, 'manageusers', db)
        
        # await ManageUsersManager().manager(update, context, edit= False)

