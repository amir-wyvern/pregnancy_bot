from cache.database import get_redis_cache


def cache(func):

    async def wrapper(*args, **kwargs):
        
        # db_cache = get_redis_cache().__next__()
        kwargs.update({'cache_db': 'db_cache'})
        result = await func(*args, **kwargs)
        return result
    
    return wrapper