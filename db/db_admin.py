from schemas import AdminRegisterForDataBase
from sqlalchemy.orm.session import Session
from db.models import DbAdmin
from typing import List


def create_admin(request: AdminRegisterForDataBase, db: Session, commit= True) -> DbAdmin:

    user = DbAdmin(
        username= request.username,
        password= request.password,
        tel_id= request.tel_id,
        status= request.status
    )
    db.add(user)

    if commit:
        db.commit()
        db.refresh(user)

    return user


def get_all_admins(db:Session) -> List[DbAdmin]:

    return db.query(DbAdmin).all()
    

def get_admin_by_admin_id(admin_id, db:Session) -> DbAdmin:
    
    return db.query(DbAdmin).filter(DbAdmin.id == admin_id ).first()


def get_admin_by_username(username, db:Session) -> DbAdmin:
    
    return db.query(DbAdmin).filter(DbAdmin.username == username ).first()
    

def update_password_by_username(username, new_password: str, db:Session ,commit= True):

    user = db.query(DbAdmin).filter(DbAdmin.username == username )
    user.update({DbAdmin.password: new_password})
    if commit:
        db.commit()
            
    return True 


def update_status_by_username(username, new_status: bool, db:Session ,commit= True):

    user = db.query(DbAdmin).filter(DbAdmin.username == username )
    user.update({DbAdmin.status: new_status})
    if commit:
        db.commit()
            
    return True 

def delete_admin_by_username(username, db:Session):

    user = get_admin_by_username(username, db)
    db.delete(user)
    db.commit()

    return True