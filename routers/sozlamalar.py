import inspect
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from functions.sozlamalar import check_limit_def
from routers.auth import current_active_user
from schemas.users import UserCurrent
from utils.role_verification import role_verification

router_sozlamalar = APIRouter()


@router_sozlamalar.get('/check_limit', status_code=200)
async def get_check_limit(db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    Buyurtma olishda joriy buyurtmalar sonini hisoblab filial limitiga solishtiradi 
    va filiyal uchun buyurtma olish yoki olmasligini aniqlab oladi
    """
    return check_limit_def(current_user, db)
