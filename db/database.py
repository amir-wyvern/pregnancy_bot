from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from configs.settings import settings

SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.SQLITE_ADDRESS}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()