from pydantic import BaseModel


class MillatResponseModel(BaseModel):
    id: int
    name: str