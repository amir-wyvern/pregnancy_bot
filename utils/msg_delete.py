from cache.cache_session import get_msg_id, remove_msg_id
from configs.settings import settings
from telegram import Bot

bot = Bot(token= settings.BOT_TOKEN)

async def msg_delete(chat_id, db):
    
    ls_msg_id = get_msg_id(chat_id, db)
    for message_id in ls_msg_id[:-1]:
        try:
            remove_msg_id(chat_id, message_id, db) 
            await bot.delete_message(chat_id=chat_id, message_id= message_id) 
            
        except:
            print('except msg: ', message_id)
    
async def msg_delete_all(chat_id, db):

    ls_msg_id = get_msg_id(chat_id, db)
    for message_id in ls_msg_id:
        try: 
            remove_msg_id(chat_id, message_id, db) 
            await bot.delete_message(chat_id=chat_id, message_id= message_id) 
        except:
            print('except msg : ', message_id)

async def one_delete_msg(chat_id, msg_id):

    try: 
        await bot.delete_message(chat_id=chat_id, message_id= msg_id) 
    except:
        print('except msg : ', msg_id)