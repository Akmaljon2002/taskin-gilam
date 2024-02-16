from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import SessionLocal
from pydantic.schema import date, time
from schemas.orders import OrderCreate

db: Session = SessionLocal()


class QaytaQongiroq(BaseModel):
    recall_date: date = None
    recall_time: time = None
    izoh: Optional[str] = None


class CostumerCreate(BaseModel):
    costumer_name: str
    costumer_phone_1: str
    costumer_phone_2: Optional[str] = None
    costumer_addres: str
    manba: Optional[str] = None
    costumer_turi: str
    izoh: Optional[str] = None
    millat_id: str
    recall: Optional[QaytaQongiroq] = None
    buyurtma: bool = False
    buyurtma_olish: Optional[OrderCreate] = None


class CostumerUpdate(BaseModel):
    id: int = Field(gt=0)
    costumer_name: str
    costumer_phone_1: str
    costumer_phone_2: str
    costumer_addres: str
    manba: str
    costumer_turi: str
    izoh: str
    millat_id: str


class UserResponce(BaseModel):
    user_id: int
    fullname: str


class OrderResponce(BaseModel):
    order_id: int
    nomer: int


class Mijoz_kirim_chiqim(BaseModel):
    order_id: Optional[OrderResponce] = None
    user_id: Optional[UserResponce] = None
    summa: int = None
    tolov_turi: str = None
    date: date = None
    status: str = None


class PaginationResponse(BaseModel):
    current_page: int
    limit: int
    pages: int
    data: Optional[Mijoz_kirim_chiqim] = None
