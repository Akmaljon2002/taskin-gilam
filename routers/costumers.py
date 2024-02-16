import inspect
from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from models.models import Costumers
from functions.costumers import all_costumers, update_costumer, create_costumer, history_costumer, nasiyalar
from routers.auth import current_active_user
from schemas.costumers import CostumerCreate, CostumerUpdate
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_costumer = APIRouter()


@router_costumer.post('/create', )
async def add_costumer(form: CostumerCreate,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_costumer(form, current_user.id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_costumer.get('/', status_code=200)
async def get_costumers(search: str = None, costumer_id: int = 0, page: int = 1,
                        limit: int = 25, db: Session = Depends(get_db)):
    if costumer_id:
        return db.query(Costumers).filter(Costumers.id == costumer_id).first()
    return all_costumers(search, page, limit, db)


@router_costumer.put("/update")
async def costumer_update(form: CostumerUpdate, db: Session = Depends(get_db)):
    if await update_costumer(form, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_costumer.get('/money_from_costumer', status_code=200)
async def money_from_costumer(search: str = None, costumer_id: int = ..., page: int = 1,
                              limit: int = 25, db: Session = Depends(get_db)):
    return history_costumer(search, page, limit, costumer_id, db)


@router_costumer.get('/nasiyalar', status_code=200)
async def money_from_costumer(search: str = None, nasiyachi_id: int = ..., page: int = 1,
                              limit: int = 25, db: Session = Depends(get_db)):
    return nasiyalar(search, page, limit, nasiyachi_id, db)
