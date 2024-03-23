from datetime import datetime, timedelta

import pytz
from fastapi import HTTPException
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import joinedload, load_only
from models.models import Orders, Mijoz_kirim, Costumers, Recall, User
from utils.pagination import pagination


# def recalls_def(page, limit, user, db):
#     six_months_ago = datetime.now() - timedelta(days=180)
#     orders = db.query(
#         Orders,
#         func.sum(Orders.order_last_price).label('total_order_last_price'),
#         func.max(Orders.top_sana).label('max_top_sana'),
#         func.max(Orders.order_id).label('max_order_id')
#     ).filter(
#         Orders.order_filial_id == user.filial_id,
#         Orders.last_operator_id == 0,
#         Orders.order_status == 'topshirildi',
#         Orders.order_date > six_months_ago
#     ).options(load_only("order_id"),
#               joinedload(Orders.costumer).options(
#                   load_only("costumer_name", "costumer_phone_1", "costumer_phone_2"))).group_by(
#         Orders.costumer_id).order_by(func.max(Orders.top_sana))
#     data = pagination(orders, page, limit)
#     data['count'] = len(data['data'])
#     return data


def recalls_def(page, limit, user, driver_id, db):
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    six_months_ago = now - timedelta(days=180)
    orders = db.query(
        Orders,
        func.max(Orders.top_sana).label('max_top_sana'),
        func.max(Orders.order_id).label('max_order_id')
    ).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id == 0,
        Orders.order_status == 'topshirildi',
        Orders.order_date > six_months_ago
    )
    driver_order_count = db.query(Orders,
        Orders.finish_driver,
        func.count(Orders.order_id).label('driver_order_count')
    ).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id == 0,
        Orders.order_status == 'topshirildi',
        Orders.order_date > six_months_ago
    ).group_by(Orders.finish_driver).order_by(func.max(Orders.top_sana))
    if driver_id:
        orders = orders.filter(Orders.finish_driver == driver_id)

    orders = orders.group_by(
        Orders.costumer_id).order_by(func.max(Orders.top_sana))
    data = pagination(orders, page, limit)
    data['yesterday_count'] = len(data['data'])
    six_month_count = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id2 == 0,
        Orders.order_date < six_months_ago,
        Orders.order_date < now - timedelta(days=2)
    ).group_by(
        Orders.costumer_id
    ).order_by(
        func.max(Orders.top_sana)
    ).count()
    data['six_month_count'] = six_month_count

    current_year = now.year

    orders_count = (
        db.query(func.count(func.distinct(Orders.costumer_id)))
        .filter(
            Orders.order_filial_id == user.filial_id,
            func.extract('year', Orders.top_sana) == current_year
        )
        .scalar()
    )

    customers_count = db.query(func.count(Costumers.id)).filter(
        Costumers.costumers_filial_id == user.filial_id).scalar()

    calling = customers_count - orders_count
    data['calling'] = calling

    recalls_count = (
        db.query(func.count(Recall.recall_id))
        .filter(
            Recall.recall_filial_id == user.filial_id,
            Recall.recall_status == 'on'
        )
        .order_by(Recall.recall_date.desc(), Recall.recall_time.desc())
        .scalar()
    )

    data['recalls_count'] = recalls_count

    data['drivers'] = driver_order_count.all()

    return data


def taking_update_def(form, user, db):
    order = db.query(Orders).filter(Orders.order_id == form.order_id, Orders.order_filial_id == user.filial_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    order.talk_type = form.mijoz_fikri.value
    order.last_izoh = form.izoh
    order.last_operator_id = user.id
    order.talk_date = datetime.now(pytz.timezone('Asia/Tashkent'))
    db.commit()
    return True
