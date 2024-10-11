from schemas import PregnancyRegisterForDataBase
from sqlalchemy.orm.session import Session
from db.models import DbPregnancy
from typing import List


def create_pregnancy(request: PregnancyRegisterForDataBase, db: Session, commit= True) -> DbPregnancy:

    pregnancy = DbPregnancy(
        user_id= request.user_id,
        date_of_pregnancy= request.date_of_pregnancy,
        baby_name= request.baby_name,
        height_before= request.height_before,
        weight_before= request.weight_before,
        height_before= request.height_before
    )
    db.add(pregnancy)

    if commit:
        db.commit()
        db.refresh(pregnancy)
    
    return pregnancy


def get_all_pregnancies(db:Session) -> List[DbPregnancy]:

    return db.query(DbPregnancy).all()
    

def get_pregnancy_by_user_id(user_id, db:Session) -> DbPregnancy:
    
    return db.query(DbPregnancy).filter(DbPregnancy.user_id == user_id ).all()


def get_pregnancy_by_pregnancy_id(pregnancy_id, db:Session) -> DbPregnancy:
    
    return db.query(DbPregnancy).filter(DbPregnancy.id == pregnancy_id ).all()


def delete_pregnancy(pregnancy_id, db:Session):

    pregnancy = get_pregnancy_by_pregnancy_id(pregnancy_id, db)
    db.delete(pregnancy)
    db.commit()

    return True