from datetime import datetime
import pytz
from fastapi import HTTPException
from functions.orders import one_order
from functions.washing import clean_first
from models.models import Clean
from schemas.washing import CleanStatus


def qadoqlash(db, filial_id, user_id, clean_id):
    clean = clean_first(db, clean_id)
    if not clean:
        raise HTTPException(status_code=400, detail="Clean not found!")
    order = one_order(clean.order_id, db)
    if not order:
        raise HTTPException(status_code=200, detail="Order not found!")
    clean.qad_user = user_id
    if clean.clean_status == "qayta quridi":
        clean.clean_status = "qayta qadoqlandi"
    else:
        clean.clean_status = "qadoqlandi"
    clean.qad_date = datetime.now(pytz.timezone('Asia/Tashkent'))
    db.commit()
    cleans = db.query(Clean).filter(
        Clean.clean_filial_id == filial_id, Clean.order_id == clean.order_id, Clean.clean_status.in_(
            [CleanStatus.QAYTA_YUVISH.value, CleanStatus.YUVILMOQDA.value, CleanStatus.OLCHOV.value,
             CleanStatus.QURIDI.value, CleanStatus.QAYTA_QURIDI.value])).count()
    if cleans == 0:
        if order.order_status == "qayta quridi":
            order.order_status = "qayta qadoqlandi"
        else:
            order.order_status = "qadoqlandi"
        db.commit()
    return {"Message": "Success", "clean": cleans}
