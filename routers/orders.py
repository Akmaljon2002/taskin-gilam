import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.orders import *
from routers.auth import current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_order = APIRouter()


@router_order.get('/', status_code=200)
async def get_orders(search: str = None, id: int = 0, page: int = 1, limit: int = 25,
                     db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_order(id, db)
    else:
        return all_orders(search, page, limit, db)
