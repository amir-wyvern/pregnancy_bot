from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional 
from enum import Enum
import re

class PhoneNumberStr(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, model, context):
        return {'type': 'string', 'format': 'phonenumber', 'example': '+98-9151234567'}
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, x):
        if not re.match(r"^\+\d{1,3}-\d{6,12}$", v):
            raise ValueError("Not a valid phone number")
        return v


class UserRole(str ,Enum):

    ADMIN = 'ADMIN'
    USER = 'USER'


class AdminRegisterForDataBase(BaseModel):

    username : str
    password: str
    tel_id: int
    status: bool

    
class UserRegisterForDataBase(BaseModel):

    name: str
    last_name: str
    phone_number: str
    tel_id: Optional[str]
    birth_date: datetime
    status: bool


class DiseaseRegisterForDataBase(BaseModel):

    user_id: int
    title: str
    start_date: datetime
    end_date: Optional[datetime]
    discription: Optional[str]


class PregnancyRegisterForDataBase(BaseModel):

    user_id: int
    date_of_pregnancy: datetime
    baby_name: Optional[str]
    height_before: Optional[float]
    weight_before: Optional[float]
    weight_current: Optional[float]
