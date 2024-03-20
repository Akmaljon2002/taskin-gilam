import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.tokcha import tokchalar_def, tokchalar_order_cleans_def
from routers.auth import current_active_user
from schemas.tokcha import TokchaResponseModel, OrderTokchaResponseModel
from schemas.users import UserCurrent
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_tokcha = APIRouter()


@router_tokcha.get('/', status_code=200)
async def get_tokchalar(page: int = 1, limit: int = 25,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[TokchaResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return tokchalar_def(page, limit, current_user.filial_id, db)


@router_tokcha.get('/order_cleans', status_code=200)
async def get_tokchalar(tokcha: str, page: int = 1, limit: int = 25,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) ->\
        PaginationResponseModel[OrderTokchaResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return tokchalar_order_cleans_def(page, limit, current_user.filial_id, tokcha, db)
