import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.branches import *
from routers.auth import current_active_user
from schemas.branches import *
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_branch = APIRouter()


# @router_branch.post('/add', )
# async def add_branch(form: BranchCreate,
#                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
#     if current_user.role != "crudadmin":
#         raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')
#     if create_branch(form, current_user.id, db):
#         raise HTTPException(status_code=200, detail="Successfully")


@router_branch.get('/', status_code=200)
async def get_branches(search: str = None, id: int = 0, page: int = 1, limit: int = 25,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if id:
        return one_branch(id, db)
    else:
        return all_branches(search, page, limit, db)


# @router_branch.put("/update")
# async def branch_update(form: BranchUpdate, db: Session = Depends(get_db),
#                         current_user: UserCurrent = Depends(get_current_active_user)):
#     if current_user.role != "crudadmin":
#         raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')
#     if update_branch(form, db):
#         raise HTTPException(status_code=200, detail="Successfully")
