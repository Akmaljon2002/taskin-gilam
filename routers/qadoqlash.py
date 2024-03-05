import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from db import get_db
from functions.washing import clean_with_status
from routers.auth import current_active_user
from schemas.users import UserCurrent
from schemas.washing import CleanStatus
from schemas.xizmatlar import XizmatQadoqlashCountResponse
from utils.role_verification import role_verification

router_qadoqlash = APIRouter()


@router_qadoqlash.get('/product', summary="Buyurtma maxsulotlarini chaqirish",
                      status_code=status.HTTP_200_OK)
async def yuvish_clean_mahsulot_get(order_id: int, db: Session = Depends(get_db),
                                    current_user: UserCurrent = Depends(current_active_user)) -> \
        XizmatQadoqlashCountResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)

    qadoqlanganlar = clean_with_status(db, order_id, [CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value])
    data = {
        'mahsulot': qadoqlanganlar,
        'qadoqlanganlar': len(qadoqlanganlar),
    }

    return data
