import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.millat import millatlar_get
from routers.auth import current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_millat = APIRouter()


@router_millat.get("/")
async def get_current_active_millat(db: Session = Depends(get_db),
                                    current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return millatlar_get(current_user, db)
