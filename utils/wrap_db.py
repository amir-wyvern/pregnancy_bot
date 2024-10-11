from db.database import get_db


def db(func):

    async def wrapper(*args, **kwargs):
        
        db = get_db().__next__()
        kwargs.update({'db': db})
        result = await func(*args, **kwargs)
        return result
    
    return wrapper
