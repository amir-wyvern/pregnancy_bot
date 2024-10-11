from schemas import AdminRegisterForDataBase, UserRole
from db.database import get_db, engine, inspect
from passlib.context import CryptContext
from db.db_admin import create_admin
from db import models
import logging 



def init_database(admin_data: AdminRegisterForDataBase, logger: logging):

     if not inspect(engine).has_table("admin"):
          models.Base.metadata.create_all(engine)
          logger.info('DataBase Created')
          
          pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
          print(1,admin_data.password )
          print(2, pwd_context.hash(admin_data.password))
          admin_data.password = pwd_context.hash(admin_data.password)
          
          create_admin(admin_data, get_db().__next__())
          logger.info('User Admin initialed!')