from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.schema import date
from schemas.xizmatlar import XizmatlarBuyurtma


class OrdersSchema(BaseModel):
    order_id: int


class XizmatChegirma(BaseModel):
    id: int
    summa: int
    chegirma_summa: int
    operator_kpi_line: int


class OrderCreate(BaseModel):
    izoh: str = None
    order_driver: Optional[str] = "hamma"
    order_skidka_foiz: int = Field(ge=0)
    order_skidka_sum: int = Field(ge=0)
    xizmat: List[XizmatChegirma]


class Order_status(Enum):
    keltirish = "keltirish"
    qabul_qilindi = "qabul qilindi"


class Order_accept(BaseModel):
    order_id: int
    topshir_sana: date = Field(...)
    brak: str = ""
    dog: str = ""
    izoh2: str = ""
    own: bool = False
    xizmatlar: List[XizmatlarBuyurtma]


class CancelOrder(BaseModel):
    order_id: int
    izoh: str
