import inspect
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from functions.operator import taking_update_def, rejadagilar_def, kechagilar_def, six_month_def, calling_def, \
    all_operators, call_report_def, recalling_def, six_month_call_report_def
from routers.auth import current_active_user
from schemas.operator import OrderCurrentlyResponseModel, PaginationResponseModel1, TalkingUpdate, \
    RejdagilarCurrentlyResponseModel, PaginationRejadagilarResponseModel1, OrderRpModel, CallingResponseModel, \
    PaginationResponseModel2, TalkingUpdateEnum, CallReportResponseModel, \
    SixMonthCallReportResponseModel
from schemas.users import UserCurrent, DriverResponseModel
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification
from utils.send_sms import SendSmsRequest, send_sms

router_operator = APIRouter()


@router_operator.get('/yesterday', status_code=200)
async def get_kechagilar(driver_id: int = 0, page: int = 1, limit: int = 25,
                         db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel1[OrderCurrentlyResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return kechagilar_def(page, limit, current_user, driver_id, db)


@router_operator.put('/talking_update', status_code=200)
async def called_order_put(form: TalkingUpdate,
                           db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    Operator izoh va mijoz fikri
    """
    if taking_update_def(form, current_user, db):
        raise HTTPException(status_code=201, detail="Successfully!")


@router_operator.get('/planning', status_code=200)
async def get_rejadagilar(operator_id: int = 0, page: int = 1, limit: int = 25,
                          db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationRejadagilarResponseModel1[RejdagilarCurrentlyResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return rejadagilar_def(page, limit, current_user, operator_id, db)


@router_operator.get('/six_month', status_code=200)
async def get_kechagilar(driver_id: int = 0, page: int = 1, limit: int = 25,
                         db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel1[OrderRpModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return six_month_def(page, limit, current_user, driver_id, db)


@router_operator.get('/calling', status_code=200)
async def get_callings(page: int = 1, limit: int = 25,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) ->\
        PaginationResponseModel2[CallingResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return calling_def(page, limit, current_user, db)


@router_operator.get('/operators', status_code=200)
async def get_users(page: int = 1, limit: int = 25,
                    db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[DriverResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return all_operators(page, limit, current_user, db)


@router_operator.get('/call_report', status_code=200)
async def get_callings(search: str = None, operator_id: int = 0, page: int = 1, limit: int = 25,
                       dan: date = None, gacha: date = None,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[RejdagilarCurrentlyResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return call_report_def(search, page, limit, current_user, operator_id, dan, gacha, db)


@router_operator.get('/recalling', status_code=200)
async def get_callings(search: str = None, q_natija: TalkingUpdateEnum = None, last_operator_id: int = 0,
                       dan: date = None, gacha: date = None, page: int = 1, limit: int = 25,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) ->\
        PaginationResponseModel[CallReportResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return recalling_def(search, q_natija, page, limit, current_user, last_operator_id, dan, gacha, db)


@router_operator.get('/six_month_call_report', status_code=200)
async def get_callings(search: str = None, q_natija: TalkingUpdateEnum = None, last_operator_id2: int = 0,
                       dan: date = None, gacha: date = None, page: int = 1, limit: int = 25,
                       db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)) ->\
        PaginationResponseModel[SixMonthCallReportResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return six_month_call_report_def(search, q_natija, page, limit, current_user, last_operator_id2, dan, gacha, db)


@router_operator.put('/send_sms', status_code=200)
async def called_order_put(form: SendSmsRequest,
                           db: Session = Depends(get_db)):
    if await send_sms(form):
        raise HTTPException(status_code=201, detail="Successfully!")

