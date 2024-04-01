from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from db import SessionLocal

db: Session = SessionLocal()


class UserCreate(BaseModel):
    username: str
    password_hash: str
    role: str
    fullname: str
    phone: int
    phone2: int
    oylik: int
    kpi: float
    maosh: float
    ozroq_kpi: float
    moi_zvonki_user_name: str
    user_moi_zvonki_address: str
    user_moi_zvonki_api: str
    zayavka_limit: int
    topshirish_limit: int
    skald_limit: int
    zakaz_status: int


class UserUpdate(BaseModel):
    user_id: int
    username: str
    password_hash: str = None
    role: str
    fullname: str
    phone: int
    phone2: int
    maosh: int


class TokenData(BaseModel):
    id: Optional[str] = None


class UserCurrent(BaseModel):
    id: int
    username: str
    password_hash: str
    role: str


class DriverResponseModel(BaseModel):
    id: int
    fullname: str


class UserResponseModel(BaseModel):
    id: int
    username: str
    role: str
    fullname: str
    phone: int
    phone2: int
    oylik: int
    kpi: float
    maosh: float
    ozroq_kpi: float
    moi_zvonki_user_name: str
    user_moi_zvonki_address: str
    user_moi_zvonki_api: str
    zayavka_limit: int
    topshirish_limit: int
    skald_limit: int
    zakaz_status: int

