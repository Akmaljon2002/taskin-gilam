from enum import Enum
from pydantic import BaseModel, model_validator
from utils.olchov import olchov

ENI_MAX, BOY_MAX, HAJM_MAX = 5, 20, 60


# /yuvilmaganlar_yuvilganlar_qadoqlanganlar ============================================================================
class Yuvilmaganlar_yuvilganlar_qadoqlanganlarResponse(BaseModel):
    yuvilmagan: int
    yuvilgan: int
    qadoqlangan: int


# Clean baza statuslari
class CleanStatus(Enum):
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


class YuvishAndQaytaYuvish(str, Enum):
    yuvish = 'yuvish'
    qayta_yuvish = 'qayta-yuvish'


class CleanResponse(BaseModel):
    id: int
    gilam_eni: float
    gilam_boyi: float
    clean_hajm: float
    clean_narx: float
    narx: int
    clean_status: str

    class Config:
        from_attributes = True


class XizmatCleanAllResponse(BaseModel):
    xizmat_id: int
    xizmat_turi: str
    olchov: str
    # cleans_count: int
    cleans: list[CleanResponse] = None

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def init_model(self) -> "Xizmat":
        self.olchov = olchov(self.olchov)
        return self


class Options(BaseModel):
    readonly: bool = False
    eni_max: int = ENI_MAX
    boyi_max: int = BOY_MAX

    class Config:
        from_attributes = True


class Xizmat(BaseModel):
    xizmat_turi: str
    olchov: str

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def init_model(self) -> "Xizmat":
        self.olchov = olchov(self.olchov)
        return self


class CleanResponse2(CleanResponse):
    xizmat: Xizmat = None
    options: Options = None

    class Config:
        from_attributes = True

    @model_validator(mode='after')
    def init_model(self) -> "CleanResponse":
        if self.clean_status == CleanStatus.QAYTA_YUVISH:
            self.options = Options(readonly=True)
        else:
            self.options = Options()

        return self


class CleanResponse3(CleanResponse):
    xizmat: Xizmat = None

    class Config:
        from_attributes = True


