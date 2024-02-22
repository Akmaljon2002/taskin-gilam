import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.transport import one_driver, all_drivers
from routers.auth import current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_transport = APIRouter()


@router_transport.get('/', status_code=200)
async def get_drivers(driver_id: int = 0,
                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if driver_id:
        return one_driver(driver_id, current_user.filial_id, db)
    return all_drivers(current_user.filial_id, db)
