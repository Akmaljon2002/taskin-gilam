from pydantic import BaseModel


class OrdersSchema(BaseModel):
    order_id: int
