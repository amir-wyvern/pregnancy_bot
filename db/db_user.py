from schemas import UserRegisterForDataBase
from sqlalchemy.orm.session import Session
from db.models import DbUser
from typing import List


def create_user(request: UserRegisterForDataBase, db: Session, commit= True) -> DbUser:

    user = DbUser(
        name= request.name,
        last_name= request.name,
        phone_number= request.phone_number,
        birth_date= request.birth_date,
        tel_id= request.tel_id,
        status= request.status
    )
    db.add(user)

    if commit:
        db.commit()
        db.refresh(user)
    
    return user


def get_all_users(db:Session) -> List[DbUser]:

    return db.query(DbUser).all()
    

def get_user_by_user_id(user_id, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.id == user_id ).first()


def get_user_by_phone_number(phone_number, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.phone_number == phone_number).first()


def update_phone_number_by_user_id(user_id, new_phone_number: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.id == user_id )
    user.update({DbUser.phone_number: new_phone_number})
    if commit:
        db.commit()    
            
    return True


def update_phone_number_by_phone_number(phone_number, new_phone_number: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.phone_number == phone_number )
    user.update({DbUser.phone_number: new_phone_number})
    if commit:
        db.commit()    
            
    return True


def update_status_by_user_id(user_id, new_status: bool, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.id == user_id )
    user.update({DbUser.status: new_status})
    if commit:
        db.commit()    
            
    return True


def delete_user(user_id, db:Session):

    user = get_user_by_user_id(user_id, db)
    db.delete(user)
    db.commit()

    return True