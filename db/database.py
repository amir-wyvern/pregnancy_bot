from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import os

SQLITE_ADDRESS = os.getenv('SQLITE_ADDRESS')

SQLALCHEMY_DATABASE_URL = f"sqlite://{SQLITE_ADDRESS}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()

sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()