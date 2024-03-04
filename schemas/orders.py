from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Union
from pydantic import BaseModel, Field, model_validator
from db import STATIC
from models.models import Clean
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


class OrderStatus(Enum):
    # Yuvish
    YUVILMOQDA = 'yuvilmoqda'
    OLCHOV = 'olchov'
    QAYTA_YUVISH = 'qayta yuvish'

    # Qadoqlash
    QURIDI = 'quridi'
    QAYTA_QURIDI = 'qayta quridi'

    # Transport (topshirish)
    QADOQLANDI = 'qadoqlandi'
    QAYTA_QADOQLANDI = 'qayta qadoqlandi'

    # Topshirildi
    TOPSHIRILDI = 'topshirildi'

    # Ombor
    OMBOR = 'ombor'

    # Keltirish
    KELTIRISH = 'keltirish'


class OrderOptionsDetail(BaseModel):
    show: bool = False
    icon: str = None

    class Config:
        from_attributes = True


class OrderOptions(BaseModel):
    saygak: Optional[OrderOptionsDetail] = None
    own: Optional[OrderOptionsDetail] = None
    res: Optional[OrderOptionsDetail] = None

    class Config:
        from_attributes = True


class Costumer(BaseModel):
    id: int
    costumer_name: str
    costumer_addres: str
    costumer_phone_1: str
    costumer_phone_2: Optional[str] = None

    class Config:
        from_attributes = True



# Funksiya
def saygak_own_res(data, icon):
    # Saygak, o'zi olip ketadiga mijozlar va qayta yuvilganlarini aniqlash
    show = False
    if data == 1:
        show = True

    return {
        "show": show,
        "icon": STATIC + '/icons/' + icon
    }


def saygak_own_res_clean(data: Clean, icon):
    show = False
    if data:
        for item in data:
            if item.clean_status == OrderStatus.QAYTA_QADOQLANDI.value:
                show = True

    return {
        "show": show,
        "icon": STATIC + '/icons/' + icon
    }


class OrderYuvishGetResponse(BaseModel):
    order_id: int
    nomer: int
    kun: int = None
    izoh: str = None
    izoh2: str = None
    topshir_sana: Union[datetime, None] = None
    costumer: Costumer
    options: Optional[OrderOptions] = None
    saygak_id: int
    own: int
    cleans_count: int = None

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def cal_kun(self) -> "OrderYuvishGetResponse":
        delay = self.topshir_sana - datetime.now()
        self.kun = delay.days
        self.options = OrderOptions(
            saygak=saygak_own_res(self.saygak_id, 'saygak.jpg'),
            own=saygak_own_res(self.own, 'own_icon.png'),
            # Shu yerni keyinroq tekshirib qo'yish kerak
            res=saygak_own_res(self.cleans_count, 'restart.png')
        )
        return self


class OrderYuvishResponse(BaseModel):
    order_id: int
    nomer: int
    izoh: str
    izoh2: str
    costumer: Costumer

    class Config:
        from_attributes = True