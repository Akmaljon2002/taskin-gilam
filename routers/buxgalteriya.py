import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.orders import order_get
from routers.auth import current_active_user
from schemas.orders import OrderYuvishGetResponse
from schemas.users import UserCurrent
from schemas.washing import CleanStatus
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_buxgalteriya = APIRouter()


@router_buxgalteriya.get('/davomat', status_code=200)
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