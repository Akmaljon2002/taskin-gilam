from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from models.models import User
from functions.users import all_users, update_user, create_user
from routers.auth import current_active_user
from schemas.users import UserCreate, UserUpdate, UserCurrent


router_user = APIRouter()


@router_user.post('/create', )
async def add_user(form: UserCreate,
                   db: Session = Depends(get_db)):
    if await create_user(form, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_user.get('/', status_code=200)
async def get_users(search: str = None, status: int = None, user_id: int = 0, role: str = None, page: int = 1,
                    limit: int = 25, db: Session = Depends(get_db)):
    if user_id:
        return db.query(User).filter(User.id == user_id).first()
    return all_users(search, status, role, page, limit, db)


@router_user.put("/update")
async def user_update(form: UserUpdate, db: Session = Depends(get_db)):
    if await update_user(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_user.get("/current_active")
async def get_current_active_user(current_user: UserCurrent = Depends(current_active_user)):
    return current_user
