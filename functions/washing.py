from datetime import datetime
import pytz
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from starlette import status
from models.models import Clean, Xizmatlar
from utils.barcode import generate_unique_number


def clean_filter_fililal_and_status_count(db, filial_id: int, status: list):
    return db.query(Clean).filter(
        Clean.clean_filial_id == filial_id,
        Clean.clean_status.in_(status)
    ).count()


def clean_select_with_xizmat(db, order_id: int, filial_id: int):
    clean = db.query(Xizmatlar) \
        .select_from(Clean) \
        .join(Xizmatlar, Clean.clean_product == Xizmatlar.xizmat_id) \
        .filter(Clean.order_id == order_id, Clean.clean_filial_id == filial_id) \
        .options(joinedload(Xizmatlar.cleans.and_(Clean.order_id == order_id))) \
        .group_by(Clean.clean_product).all()

    if clean is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu id bo'yicha ma'lumot topilmadi")

    return clean


def clean_with_status(db, order_id: int, status: list):
    return db.query(Clean).filter(Clean.order_id == order_id, Clean.clean_status.in_(status)).options(
        joinedload(Clean.xizmat)).all()


def insert_clean(db, data: dict):
    query = Clean(
        order_id=data['order_id'],
        clean_filial_id=data['clean_filial_id'],
        costumer_id=data['costumer_id'],
        clean_product=data['clean_product'],
        clean_status=data['clean_status'],
        clean_hajm=data['clean_hajm'],
        barcode=generate_unique_number(),
        narx=0,
        clean_narx=0,
        user_id=0,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
        updated_at='0000-00-00 00:00:00'
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def clean_first(db, id: int):
    return db.query(Clean).filter(Clean.id == id).options(
        joinedload(Clean.xizmat)).first()


def update_clean(db, id: int, data: dict):
    query = db.query(Clean).filter(Clean.id == id).update(data)
    db.commit()
    return query
