from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from models.models import Clean, Orders
from schemas.washing import CleanStatus
from utils.pagination import pagination


def tokchalar_def(page, limit, filial_id, db):
    tokchalar = db.query(func.upper(Clean.joy).label('joy'), func.count(Clean.id).label('total')).filter(
        Clean.clean_filial_id == filial_id, Clean.joy != "",
        Clean.clean_status.in_([CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value])
    ).group_by(Clean.joy)
    return pagination(tokchalar, page, limit)


def tokchalar_order_cleans_def(page, limit, filial_id, tokcha, db):
    orders = db.query(Orders).join(Clean).filter(
        Orders.order_filial_id == filial_id, Clean.clean_status.in_([CleanStatus.QADOQLANDI.value,
                                                                     CleanStatus.QAYTA_QADOQLANDI.value]),
        Clean.joy == tokcha).options(joinedload(Orders.cleans.and_(Clean.joy == tokcha,
                                                                   Clean.clean_status.in_([
                                                                       CleanStatus.QADOQLANDI.value,
                                                                       CleanStatus.QAYTA_QADOQLANDI.value])))).group_by(
        Orders.order_id).having(func.count(Clean.id) > 0)

    return pagination(orders, page, limit)


def tokcha_update(tokcha, clean_id, filial_id, db):
    clean = db.query(Clean).filter(Clean.id == clean_id, Clean.clean_filial_id == filial_id).first()
    if not clean:
        raise HTTPException(status_code=400, detail="Clean not found!")

    clean.joy = tokcha
    db.commit()
    return True
