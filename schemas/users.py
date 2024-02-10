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
    ozroq_kpi: float
    moi_zvonki_user_name: str
    user_moi_zvonki_address: str
    user_moi_zvonki_api: str


class UserUpdate(BaseModel):
    user_id: int
    username: str
    password_hash: str
    role: str
    fullname: str
    phone: int
    phone2: int
    maosh: int


class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None


class UserCurrent(BaseModel):
    id: int
    username: str
    password: str
    role: str
    is_active: bool
