from configs.settings import settings 
import redis

class RedisSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, url):
        if not hasattr(self, '_redis_db'):
            print(url)
            self._redis_db = redis.Redis(
                host='localhost',  # Adjust this if your Redis server is elsewhere
                port=6379,
                decode_responses=True
            )

            # self._redis_db = redis.Redis.from_url(url, decode_responses=True)
            
    @property
    def redis_db(self):
        return self._redis_db


session = RedisSingleton(settings.CACHE_URL)


def get_redis_cache():
    try:
        yield session.redis_db

    finally:
        session.redis_db.close()
