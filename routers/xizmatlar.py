import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.xizmatlar import *
from routers.auth import current_active_user
from schemas.xizmatlar import *
from schemas.users import UserCurrent
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_xizmat = APIRouter()


# @router_xizmat.post('/add', )
# async def add_xizmat(form: XizmatCreate,
#                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
#     if current_user.role != "crudadmin":
#         raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')
#     if create_xizmat(form, current_user.id, db):
#         raise HTTPException(status_code=200, detail="Successfully")


@router_xizmat.get('/', status_code=200)
async def get_xizmatlar(search: str = None, id: int = 0, page: int = 1, limit: int = 25,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[XizmatlarResponceModel] | XizmatlarResponceModel:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_xizmat(id, current_user.filial_id, db)
    else:
        return all_xizmatlar(search, page, limit, current_user.filial_id, db)

# @router_xizmat.put("/update")
# async def xizmat_update(form: XizmatUpdate, db: Session = Depends(get_db),
#                         current_user: UserCurrent = Depends(get_current_active_user)):
#     if current_user.role != "crudadmin":
#         raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')
#     if update_xizmat(form, db):
#         raise HTTPException(status_code=200, detail="Successfully")
