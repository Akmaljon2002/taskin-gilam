from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import SessionLocal

db: Session = SessionLocal()


class CostumerCreate(BaseModel):
    costumer_name: str
    costumer_phone_1: str
    costumer_phone_2: str
    costumer_addres: str
    manba: str
    costumer_turi: str
    izoh: str
    millat_id: str


class CostumerUpdate(BaseModel):
    id: int = Field(e=0.1)
    costumer_name: str
    costumer_phone_1: str
    costumer_phone_2: str
    costumer_addres: str
    manba: str
    costumer_turi: str
    izoh: str
    millat_id: str
