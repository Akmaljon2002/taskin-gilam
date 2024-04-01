import inspect
from typing import List
from fastapi import APIRouter, Depends
from db import get_db
from functions.xizmatlar import *
from routers.auth import current_active_user
from schemas.xizmatlar import *
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_xizmat = APIRouter()


@router_xizmat.post('/add', )
async def add_xizmat(form: XizmatCreate,
                     db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_xizmat(form, current_user, db):
        raise HTTPException(status_code=200, detail="Successfully")


@router_xizmat.get('/', status_code=200)
async def get_xizmatlar(db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        List[XizmatlarResponceModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return all_xizmatlar(current_user.filial_id, db)


@router_xizmat.put("/update")
async def xizmat_update(form: XizmatUpdate, db: Session = Depends(get_db),
                        current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if update_xizmat(form, current_user, db):
        raise HTTPException(status_code=200, detail="Successfully")
