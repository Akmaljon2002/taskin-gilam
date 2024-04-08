from datetime import datetime

from pydantic import BaseModel

from schemas.users import DriverResponseModel


class HisobPost(BaseModel):
    user_id: int
    kirim_summ: int
    chiqim_summ: int
    chiqim_firma: int
    chiqim_shaxsiy: int
    chiqim_izoh: str


class KirimlarResponseModel(BaseModel):
    kirim_id: int
    kassachi_id: int
    tolov_turi: str
    kirim_user_id: int
    kirim_summ: int
    kirim_date: datetime
    kassachi: DriverResponseModel
    hodim: DriverResponseModel
