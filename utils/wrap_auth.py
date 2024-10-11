from cache.cache_session import get_session, set_position
from db.db_admin import get_admin_by_tel_id
from methods.login import LoginManager

def auth(func):

    async def wrapper(*args, **kwargs):

        db = kwargs.get('db', None)
        cache_db = kwargs.get('cache_db', None)

        if db is None:
            raise 'db decorator is not used'


        if hasattr(args[1], '_chat_id'):
            chat_id = args[1]._chat_id
            _args = args

        else:
            chat_id = args[1].effective_chat.id
            _args = args[1:]

        admin = get_admin_by_tel_id(chat_id, db)
        
        if admin == None or admin.status == False:
            raise "not authentication"

        session = get_session(chat_id, cache_db)
        if session is None:

            set_position(chat_id, 'login_manager', cache_db)

            await LoginManager().manager(*_args, db= db, cache_db= cache_db)
            return


        result = await func(*args, **kwargs)
        return result

    return wrapper

