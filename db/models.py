from db.database import Base
from sqlalchemy import (
    Float,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship


class DbUser(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(String(50), index=True, unique=True, nullable=False)
    name = Column(String(50), index=True, nullable=False)
    last_name = Column(String(50), index=True, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    tel_id = Column(Integer, nullable=True, unique=True) 
    status = Column(Boolean, nullable=False)

    pregnancies_rel = relationship("DbPregnancy", back_populates="user_rel")
    diseases_rel = relationship("DbDisease", back_populates="user_rel")


class DbPregnancy(Base):

    __tablename__ = 'pregnancy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    date_of_pregnancy = Column(DateTime, nullable=False)
    baby_name = Column(String(50), nullable=True)
    height_before = Column(Float, nullable=True)
    weight_before = Column(Float, nullable=True)
    weight_current = Column(Float, nullable=True)

    user_rel = relationship("DbUser", back_populates="pregnancies_rel")


class DbDisease(Base):

    __tablename__ = 'disease'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    title = Column(String(100), index=True, nullable=False)
    start_date = Column(DateTime, nullable=False)
    start_end = Column(DateTime, nullable=True)
    discription = Column(String(500), nullable= True)

    user_rel = relationship("DbUser", back_populates="diseases_rel")


class DbAdmin(Base):

    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique= True)
    password = Column(String(100), nullable=False) 
    tel_id = Column(Integer, nullable=False, unique=True) 
    status = Column(Boolean, nullable=False)


