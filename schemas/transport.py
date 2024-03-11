from pydantic import BaseModel


class BuyurtmaSkladTopshiriladiganResponse(BaseModel):
    buyurtmalar: int
    sklad: int
    topshiriladigan: int