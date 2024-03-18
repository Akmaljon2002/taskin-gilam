import inspect
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from models.models import Costumers
from functions.costumers import all_costumers, update_costumer, create_costumer, history_costumer, nasiyalar, \
    nasiyachilar, nasiyalar_all, nasiya_olish, nasiya_kechish, nasiyalar_tasdiqlanmagan_all, nasiya_tasdiqlash, \
    create_costumer_order
from routers.auth import current_active_user
from schemas.costumers import CostumerCreate, CostumerUpdate, NasiyachiResponseModel, NasiyalarResponseModel, \
    NasiyaOlish, CostumerResponseModel, CostumerCreateOrder
from schemas.users import UserCurrent
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_costumer = APIRouter()


@router_costumer.post('/create_order', )
async def add_costumer(form: CostumerCreateOrder,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_costumer_order(form, current_user.id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_costumer.post('/create', )
async def add_costumer(form: CostumerCreate,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if create_costumer(form, current_user.id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Created successfully!")


@router_costumer.get('/', status_code=200)
async def get_costumers(search: str = None, costumer_id: int = 0, page: int = 1,
                        limit: int = 25, db: Session = Depends(get_db)) -> \
        PaginationResponseModel[CostumerResponseModel]:
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
async def nasiyalar_get(search: str = None, nasiyachi_id: int = ..., page: int = 1,
                        limit: int = 25, db: Session = Depends(get_db)):
    return nasiyalar(search, page, limit, nasiyachi_id, db)


@router_costumer.get('/nasiyachilar', status_code=200)
async def nasiyachilar_get(db: Session = Depends(get_db),
                           current_user: UserCurrent = Depends(current_active_user)) -> List[NasiyachiResponseModel]:
    return nasiyachilar(current_user.filial_id, db)


@router_costumer.get('/nasiyalar_all', status_code=200)
async def nasiyalar_all_get(search: str = None, nasiyachi_id: int = 0, page: int = 1,
                            limit: int = 25, db: Session = Depends(get_db),
                            current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[NasiyalarResponseModel]:
    return nasiyalar_all(search, page, limit, nasiyachi_id, current_user.filial_id, db)


@router_costumer.put("/nasiya_olish")
async def costumer_update(form: NasiyaOlish, db: Session = Depends(get_db),
                          current_user: UserCurrent = Depends(current_active_user)):
    if nasiya_olish(form, current_user, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_costumer.put("/nasiya_kechish")
async def costumer_update(nasiya_id: int, db: Session = Depends(get_db),
                          current_user: UserCurrent = Depends(current_active_user)):
    if nasiya_kechish(nasiya_id, current_user, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")


@router_costumer.get('/nasiya_tasdiqlanmaganlar', status_code=200)
async def nasiyalar_tasdiqlanmagan_get(page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                                       current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[NasiyalarResponseModel]:
    """
    Nasiyaga yozilib tasdiqlanmaganlar keladi
    """
    return nasiyalar_tasdiqlanmagan_all(page, limit, current_user.filial_id, db)


@router_costumer.put("/nasiya_tasdiqlash")
async def costumer_update(nasiya_id: int, ber_date: date, db: Session = Depends(get_db),
                          current_user: UserCurrent = Depends(current_active_user)):
    """
    Nasiyaga yozilib tasdiqlanmagan nasiyalarni tasdiqlash
    """
    if nasiya_tasdiqlash(nasiya_id, ber_date, db):
        raise HTTPException(status_code=200, detail="Updated successfully!")
