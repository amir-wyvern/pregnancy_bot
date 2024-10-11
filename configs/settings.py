from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    BOT_TOKEN: str
    CACHE_URL: str
    SQLITE_ADDRESS: str

    class Config:
        env_file = '.env'

settings = Settings()
