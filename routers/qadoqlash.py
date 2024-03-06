import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from db import get_db
from functions.orders import order_get
from functions.qadoqlash import qadoqlash
from functions.washing import clean_with_status
from routers.auth import current_active_user
from schemas.orders import OrderYuvishGetResponse
from schemas.users import UserCurrent
from schemas.washing import CleanStatus
from schemas.xizmatlar import XizmatQadoqlashCountResponse
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_qadoqlash = APIRouter()


@router_qadoqlash.get('/quridi_and_qayta', status_code=200)
async def yuvish_get(page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[OrderYuvishGetResponse]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Qurigan va qayta qurigan buyurtmlarni chaqirib olamiz
    """

    data = order_get(page, limit, db, current_user.filial_id, [
        CleanStatus.QURIDI.value,
        CleanStatus.QAYTA_QURIDI.value
    ])

    return data


@router_qadoqlash.get('/product', summary="Buyurtma maxsulotlarini chaqirish",
                      status_code=status.HTTP_200_OK)
async def yuvish_clean_mahsulot_get(order_id: int, db: Session = Depends(get_db),
                                    current_user: UserCurrent = Depends(current_active_user)) -> \
        XizmatQadoqlashCountResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)

    qadoqlanganlar = clean_with_status(db, order_id, [CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value])
    quriganlar = clean_with_status(db, order_id, [CleanStatus.QURIDI.value, CleanStatus.QAYTA_QURIDI.value])
    data = {
        'qadoqlanganlar': qadoqlanganlar,
        'yuvilganlar': quriganlar
    }
    return data


@router_qadoqlash.put('/update_qadoqlash', status_code=status.HTTP_202_ACCEPTED)
async def qadoqlash_update(clean_id: int, db: Session = Depends(get_db),
                           current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Clean qayta yuvishga ozgartirish
    """

    data = qadoqlash(db, current_user.filial_id, current_user.id, clean_id)
    return data
