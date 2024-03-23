from datetime import datetime
from enum import Enum
from typing import Optional, List, Generic
from pydantic import BaseModel
from pydantic.generics import GenericModel
from schemas.orders import Costumer
from schemas.users import DriverResponseModel
from utils.pagination import DataType


class OrderDriverModel(BaseModel):
    f_driver: Optional[DriverResponseModel]


class DriverCurrentlyResponseModel(BaseModel):
    Orders: Optional[OrderDriverModel]
    driver_order_count: int


class PaginationResponseModel1(GenericModel, Generic[DataType]):
    current_page: int
    limit: int
    pages: int
    yesterday_count: int
    six_month_count: int
    calling: int
    recalls_count: int
    drivers: List[DriverCurrentlyResponseModel]
    data: List[DataType] = None

    class Config:
        orm_mode = True


class OrderRpModel(BaseModel):
    order_id: int
    mijoz_kirim_summa: int
    costumer: Optional[Costumer]


class OrderCurrentlyResponseModel(BaseModel):
    max_top_sana: datetime
    max_order_id: int
    Orders: Optional[OrderRpModel]


class TalkingUpdateEnum(Enum):
    ijobiy = "ijobiy"
    salbiy = "salbiy"
    etiroz = "e`tiroz"


class TalkingUpdate(BaseModel):
    order_id: int
    izoh: str
    mijoz_fikri: Optional[TalkingUpdateEnum]
