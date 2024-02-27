import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.orders import *
from routers.auth import current_active_user
from schemas.orders import Order_status, Order_accept, CancelOrder
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_order = APIRouter()


@router_order.get('/', status_code=200)
async def get_orders(search: str = None, order_id: int = 0, page: int = 1, limit: int = 25,
                     db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if order_id:
        return one_order(order_id, db)
    return all_orders(search, page, limit, db)


@router_order.get('/to_drivers', status_code=200)
async def get_orders_driver(status: Order_status, search: str = None, order_id: int = 0, page: int = 1, limit: int = 25,
                            db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if order_id:
        return order_to_drivers(order_id, db)
    return orders_to_drivers(search, page, limit, current_user.id, status, db)


@router_order.get('/recleans', status_code=200)
async def get_orders_driver(search: str = None, clean_id: int = 0, page: int = 1, limit: int = 25,
                            db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if clean_id:
        return reclean(clean_id, db)
    return recleans(search, page, limit, current_user.id, db)


@router_order.put('/accept', status_code=200)
async def accept_order_driver(form: Order_accept,
                              db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if accept_order(form, current_user.id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Successfully!")


@router_order.put('/edit_driver', status_code=200)
async def edit_driver_order(order_id: int, driver_id: int = 0,
                            db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if edit_order_driver(order_id, driver_id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Successfully!")


@router_order.put('/cancel', status_code=200)
async def cancel_order_update(form: CancelOrder,
                              db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if cancel_order(form, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Successfully!")


@router_order.put('/called', status_code=200)
async def called_order_put(order_id: int,
                           db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if called_order(order_id, current_user.filial_id, db):
        raise HTTPException(status_code=201, detail="Successfully!")
