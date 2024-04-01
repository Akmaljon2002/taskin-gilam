import inspect

from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from models.models import User
from functions.users import all_users, update_user, create_user
from routers.auth import current_active_user
from schemas.users import UserCreate, UserUpdate, UserCurrent, UserResponseModel
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_user = APIRouter()


@router_user.post('/create', )
async def add_user(form: UserCreate,
                   db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if await create_user(form, current_user, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_user.get('/', status_code=200)
async def get_users(search: str = None, status: int = None, user_id: int = 0, role: str = None, page: int = 1,
                    limit: int = 25, db: Session = Depends(get_db),
                    current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[UserResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return all_users(search, status, role, page, limit, current_user, db)


@router_user.put("/update")
async def user_update(form: UserUpdate, db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if await update_user(form, current_user, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_user.get("/current_active")
async def get_current_active_user(current_user: UserCurrent = Depends(current_active_user)):
    return current_user


@router_user.get("/rollar")
async def get_current_active_user(current_user: UserCurrent = Depends(current_active_user)):
    data = {
        'admin_filial': 'Filial admin',
        'hisobchi': 'Hisobchi',
        'operator': 'Operator',
        'transport': 'Transport',
        'yuvish': 'Yuvish',
        'yuvish_adiyol': 'Yuvish adiyol',
        'tayorlov': 'Qadoqlash',
        'joyida_yuvish': 'Joyida yuvish',
        'saygak': 'Saygak',
        'admin_savdo': 'Savdo admin'
    }
    return data


@router_user.get("/tolov_turi")
async def get_current_active_user(current_user: UserCurrent = Depends(current_active_user)):
    data = {
        'naqd': 'Naqd',
        'click': 'Click',
        'Terminal-bank': 'Terminal-bank'
    }
    return data
