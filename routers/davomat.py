import inspect
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from functions.davomat import davomatlar_def, davomat_update_def
from routers.auth import current_active_user
from schemas.davomat import DavomatResponseModel, StatusDavomatEnum
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_davomat = APIRouter()


@router_davomat.get('/', status_code=200)
async def devomat_get(sana: date = None, db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(current_active_user)) -> List[DavomatResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    Bughalteriya -> Davomat
    """

    return davomatlar_def(current_user, sana, db)


@router_davomat.put('/update', status_code=200)
async def davomat_update_put(davomat_id: List[int], status: StatusDavomatEnum, db: Session = Depends(get_db),
                             current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
        Bughalteriya -> Davomat
    """
    if davomat_update_def(davomat_id, current_user, status.value, db):
        raise HTTPException(status_code=201, detail="Successfully!")
