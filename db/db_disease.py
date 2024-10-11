from schemas import DiseaseRegisterForDataBase
from sqlalchemy.orm.session import Session
from db.models import DbDisease
from typing import List


def create_disease(request: DiseaseRegisterForDataBase, db: Session, commit= True) -> DbDisease:

    disease = DbDisease(
        title= request.title,
        start_date= request.start_date,
        end_date= request.end_date,
        discription= request.discription
    )
    db.add(disease)

    if commit:
        db.commit()
        db.refresh(disease)
    
    return disease


def get_all_diseases(db:Session) -> List[DbDisease]:

    return db.query(DbDisease).all()
    

def get_diseases_by_user_id(user_id, db:Session) -> DbDisease:
    
    return db.query(DbDisease).filter(DbDisease.user_id == user_id ).all()


def get_diseases_by_disease_id(disease_id, db:Session) -> DbDisease:
    
    return db.query(DbDisease).filter(DbDisease.id == disease_id ).all()


def get_diseases_by_title(title, db:Session) -> DbDisease:
    
    return db.query(DbDisease).filter(DbDisease.title == title).all()


def delete_disease(disease_id, db:Session):

    disease = get_diseases_by_disease_id(disease_id, db)
    db.delete(disease)
    db.commit()

    return True