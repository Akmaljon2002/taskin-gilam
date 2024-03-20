from typing import Optional, List

from pydantic import BaseModel

from schemas.orders import Costumer, Clean1


class TokchaResponseModel(BaseModel):
    joy: str
    total: int


class OrderTokchaResponseModel(BaseModel):
    order_id: int
    nomer: int
    order_status: str
    cleans_count: int = None
    costumer: Optional[Costumer]
    cleans: List[Clean1]

