import inspect
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from functions.operator import recalls_def, taking_update_def
from routers.auth import current_active_user
from schemas.operator import OrderCurrentlyResponseModel, PaginationResponseModel1, TalkingUpdate
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_operator = APIRouter()


@router_operator.get('/', status_code=200)
async def get_recalls(driver_id: int = 0, page: int = 1, limit: int = 25,
                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel1[OrderCurrentlyResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return recalls_def(page, limit, current_user, driver_id, db)


@router_operator.put('/talking_update', status_code=200)
async def called_order_put(form: TalkingUpdate,
                           db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    Operator izoh va mijoz fikri
    """
    if taking_update_def(form, current_user, db):
        raise HTTPException(status_code=201, detail="Successfully!")
