from datetime import datetime
import pytz
from models.models import Buyurtma


def select_buyurtma_first(db, id: int = None, filial_id: int = None, x_id: int = None, order_id: int = None):
    query = db.query(Buyurtma)
    if id:
        query = query.filter(Buyurtma.id == id)
    if filial_id:
        query = query.filter(Buyurtma.filial_id == filial_id)
    if x_id:
        query = query.filter(Buyurtma.x_id == x_id)
    if order_id:
        query = query.filter(Buyurtma.order_id == order_id)

    data = query.first()

    return data


def update_buyurtma_value(db, id: int, value: int):
    value += 1
    query = db.query(Buyurtma).filter(Buyurtma.id == id).update({'value': value})
    db.commit()
    return query


def insert_buyurtma(db, data: dict):
    query = Buyurtma(
        filial_id=data['filial_id'],
        x_id=data['x_id'],
        order_id=data['order_id'],
        value=1,
        status=2,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
        updated_at="1000-01-01 00:00:00"
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query
