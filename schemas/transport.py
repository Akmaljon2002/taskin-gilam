from pydantic import BaseModel
from schemas.costumers import TolovTuri


class BuyurtmaSkladTopshiriladiganResponse(BaseModel):
    buyurtmalar: int
    sklad: int
    topshiriladigan: int


class TopshirishSchema(BaseModel):
    order_id: int
    tolov_turi: TolovTuri
    summa: int
