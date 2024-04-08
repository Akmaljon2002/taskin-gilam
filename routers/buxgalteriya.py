import inspect
from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from functions.buxgalteriya import kirimlar_def, kirim_olindi, filter_uchun_hodimlar, kassa_kirimlar_get_def
from routers.auth import current_active_user
from schemas.buxgalteriya import HisobPost, KirimlarResponseModel
from schemas.users import UserCurrent, UserForKirimResponseModel, DriverResponseModel
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_buxgalteriya = APIRouter()


@router_buxgalteriya.get('/kirimlar', status_code=200)
async def kirimlar_get(page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                       current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[UserForKirimResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buhgalteriya -> Kirimlar
    """

    return kirimlar_def(page, limit, current_user, db)


@router_buxgalteriya.put('/olindi', status_code=200)
async def davomat_update_put(form: HisobPost, db: Session = Depends(get_db),
                             current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
        Bughalteriya -> Kirim -> Olindi
    """
    if kirim_olindi(current_user, form, db):
        raise HTTPException(status_code=201, detail="Successfully!")


@router_buxgalteriya.get('/hodimlar', status_code=200)
async def hodimlar_kirim_uchun(db: Session = Depends(get_db),
                               current_user: UserCurrent = Depends(current_active_user)) -> List[DriverResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buhgalteriya -> Kirimlar
    """

    return filter_uchun_hodimlar(current_user, db)


@router_buxgalteriya.get('/kassa_kirimlar', status_code=200)
async def kassa_kirimlar_get(kassachi_top: int = 0, kassachi_id: int = 0, search: str = None, sana: date = None,
                             page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                             current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[KirimlarResponseModel]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buhgalteriya -> Kirimlar
    """

    return kassa_kirimlar_get_def(search, page, limit, current_user, sana, kassachi_id, kassachi_top, db)


# @router_buxgalteriya.get('/mijoz_kirim', status_code=200)
# async def kassa_kirimlar_get(search: str = None, sana: date = None,
#                              page: int = 1, limit: int = 25, db: Session = Depends(get_db),
#                              current_user: UserCurrent = Depends(current_active_user)) -> \
#         PaginationResponseModel[KirimlarResponseModel]:
#     role_verification(current_user, inspect.currentframe().f_code.co_name)
#     """
#     ## Buhgalteriya -> Kirimlar
#     """
#
#     return kassa_kirimlar_get_def(search, page, limit, current_user, sana, db)
