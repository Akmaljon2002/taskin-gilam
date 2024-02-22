from sqlalchemy import or_
from models.models import User, Orders, Clean


def all_drivers(filial_id, db):
    data = db.query(User).filter(
        User.filial_id == filial_id, or_(User.role == "transport", User.role == "joyida_yuvish")
    ).all()

    k_count = 0
    t_count = 0
    drivers = []
    for item in data:
        order = db.query(Orders).filter(Orders.order_driver == item.id)

        k_count += order.filter(Orders.order_status == "keltirish").count()
        k_count += db.query(Clean).join(Clean.order).filter(
            Clean.clean_status == "qayta keltirish", Orders.order_driver == item.id
        ).count()

        t_count += order.filter(
            or_(Orders.order_status == "qadoqlandi", Orders.order_status == "qayta qadoqlandi")
        ).count()

        if item.zayavka_limit > k_count and item.topshirish_limit > t_count or item.role == "joyida_yuvish":
            drivers.append(item)

    return drivers


def one_driver(driver_id, filial_id, db):
    return db.query(User).filter(User.id == driver_id, User.filial_id == filial_id).first()
