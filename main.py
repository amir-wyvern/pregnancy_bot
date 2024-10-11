import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

from configs.settings import settings

from handlers.start_handler import start
# from handlers.command_handler import logout

from handlers.callback_handler import callback_handler
from handlers.message_handler import message_handler

from db.initial import init_database
from schemas import AdminRegisterForDataBase


root_logger = logging.getLogger()
root_logger.handlers.clear()

admin_default = AdminRegisterForDataBase(
    username= settings.ADMIN_USERNAME_DEFAULT,
    password= settings.ADMIN_PASSWORD_DEFAULT,
    tel_id= settings.ADMIN_TEL_ID_DEFAULT,
    status= True
)

init_database(admin_default, root_logger)

if __name__ == '__main__':

    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    # application.add_handler(CommandHandler('logout', logout))
    application.add_handler(MessageHandler(filters.TEXT, message_handler))
    # application.add_handler(MessageHandler(filters.CONTACT, phonenumber_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    application.run_polling()
