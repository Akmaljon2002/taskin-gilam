from datetime import date
from pydantic import BaseModel, Field


class BranchCreate(BaseModel):
    filial_name: str
    filial_address: str
    filial_phone: str
    filial_destination: str
    filial_status: str
    filial_director_id: int
    filial_work_date: date
    comment: str
    status: bool
    deadline: date


class BranchUpdate(BaseModel):
    id: int = Field(gt=0)
    name: str
    admin_id: int = Field(gt=0)
    address: str
    comment: str
    status: bool
    deadline: date
