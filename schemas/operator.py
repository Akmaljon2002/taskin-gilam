from datetime import datetime, date, time, timedelta
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
    rejadagilar_count: int
    drivers: List[DriverCurrentlyResponseModel]
    data: List[DataType] = None

    class Config:
        from_attributes = True


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


class RejdagilarCurrentlyResponseModel(BaseModel):
    recall_id: int
    recall_date: date
    recall_time: timedelta
    izoh: str
    costumer: Optional[Costumer]


class RecallOperatorModel(BaseModel):
    operator: Optional[DriverResponseModel]


class OperatorCurrentlyResponseModel(BaseModel):
    Recall: Optional[RecallOperatorModel]
    operator_count: int


class PaginationRejadagilarResponseModel1(GenericModel, Generic[DataType]):
    current_page: int
    limit: int
    pages: int
    yesterday_count: int
    six_month_count: int
    calling: int
    rejadagilar_count: int
    yashil_count: int
    sariq_count: int
    qizil_count: int
    operators: List[OperatorCurrentlyResponseModel]
    data: List[DataType] = None

    class Config:
        from_attributes = True


class OrderSixMonthCurrentlyResponseModel(BaseModel):
    Orders: Optional[OrderRpModel]


class CallingResponseModel(BaseModel):
    id: int
    costumer_name: str
    costumer_phone_1: str
    costumer_phone_2: str
    calling: bool


class PaginationResponseModel2(GenericModel, Generic[DataType]):
    current_page: int
    limit: int
    pages: int
    yesterday_count: int
    six_month_count: int
    calling: int
    rejadagilar_count: int
    data: List[DataType] = None

    class Config:
        from_attributes = True


class Last_operator2ResponseModel(BaseModel):
    id: int
    fullname: str


class CallReportResponseModel(BaseModel):
    order_id: int
    nomer: int
    talk_date: datetime | str
    talk_date2: datetime | str
    last_izoh2: str
    last_izoh: str
    talk_type2: str
    talk_type: str
    last_operator: Optional[Last_operator2ResponseModel]
    costumer: Optional[Costumer]


class SixMonthCallReportResponseModel(BaseModel):
    order_id: int
    nomer: int
    talk_date: datetime | str
    talk_date2: datetime | str
    last_izoh2: str
    last_izoh: str
    talk_type2: str
    talk_type: str
    last_operator2: Optional[Last_operator2ResponseModel]
    costumer: Optional[Costumer]
