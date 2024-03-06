from pydantic import BaseModel
from schemas.washing import CleanResponse3


class XizmatQadoqlashCountResponse(BaseModel):
    qadoqlanganlar: list[CleanResponse3] = None
    yuvilganlar: list[CleanResponse3] = None

    class Config:
        from_attributes = True
