from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from db import SessionLocal
from schemas.washing import XizmatCleanAllResponse, CleanResponse2, ENI_MAX, BOY_MAX, HAJM_MAX, CleanResponse3

db: Session = SessionLocal()


class XizmatlarBuyurtma(BaseModel):
    xizmat_id: int
    quantity: int


class XizmatlarResponceModel(BaseModel):
    xizmat_id: int
    filial_id: int
    narx: int
    min_narx: int
    discount_for_own: int
    xizmat_turi: str
    status: str
    olchov: str
    saygak_narx: int
    operator_kpi_line: int
    created_at: datetime
    updated_at: str

    class Config:
        from_attributes = True


class XizmatStatus(Enum):
    ACTIVE = 'active'
    DISACTIVE = 'disactive'


class XizmatCleanCountResponse(BaseModel):
    mahsulot_all: List[XizmatCleanAllResponse] = None
    mahsulot: List[CleanResponse2] = None
    yuvilmagan: int

    class Config:
        from_attributes = True


class XizmatQuridiCountResponse(BaseModel):
    mahsulot: List[CleanResponse3] = None
    quriganlar: int

    class Config:
        from_attributes = True


class XizmatYuvishPost(BaseModel):
    xizmat_id: int = Field(...)
    costumer_id: int = Field(...)


class XizmatYuvishPut(BaseModel):
    clean_id: int
    eni: float = Field(..., le=ENI_MAX)
    boy: float = Field(..., le=BOY_MAX)
    hajm: float = Field(..., le=HAJM_MAX)
    narx: float


class XizmatTuriEnum(Enum):
    kilogramm = "kilogramm"
    kv_metr = "kv metr"
    metr = "metr"
    dona = "dona"


class XizmatCreate(BaseModel):
    xizmat_turi: str
    olchov: XizmatTuriEnum
    status: XizmatStatus
    operator_kpi_line: int
    narx: int
    min_narx: int
    discount_for_own: int
    saygak_narx: int


class XizmatUpdate(BaseModel):
    xizmat_id: int
    xizmat_turi: str
    olchov: XizmatTuriEnum
    status: XizmatStatus
    operator_kpi_line: int
    narx: int
    min_narx: int
    discount_for_own: int
    saygak_narx: int

