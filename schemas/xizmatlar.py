from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import SessionLocal

db: Session = SessionLocal()


class XizmatlarBuyurtma(BaseModel):
    xizmat_id: int
    quantity: int
