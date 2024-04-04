from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel


class UserResponseModel(BaseModel):
    id: int
    username: str
    role: str
    fullname: str
    phone: int
    phone2: int
    oylik: int
    maosh: float


class DavomatResponseModel(BaseModel):
    id: int
    sana: date
    ketdi: bool
    keldi: bool
    user: Optional[UserResponseModel]


class StatusDavomatEnum(Enum):
    keldi = "keldi"
    yarim = "yarim"
    butun = "butun"