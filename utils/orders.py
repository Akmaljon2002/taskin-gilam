from datetime import datetime
import pytz
from sqlalchemy import extract
from models.models import Orders


def order_nomer(db):
    year = datetime.now(pytz.timezone('Asia/Tashkent')).year
    last_order = db.query(Orders).filter(extract('year', Orders.order_date) == year).order_by(Orders.nomer.desc()).first()
    if last_order:
        nomer = last_order.nomer + 1
    else:
        nomer = 1
    return nomer


