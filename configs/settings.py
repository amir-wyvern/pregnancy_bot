from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    BOT_TOKEN: str
    CACHE_URL: str
    SQLITE_ADDRESS: str

    ADMIN_USERNAME_DEFAULT: str
    ADMIN_PASSWORD_DEFAULT: str
    ADMIN_TEL_ID_DEFAULT: int
    
    class Config:
        env_file = '.env'

settings = Settings()
