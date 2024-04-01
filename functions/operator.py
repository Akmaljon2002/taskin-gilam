from datetime import datetime, timedelta
import pytz
from fastapi import HTTPException
from sqlalchemy import func
from models.models import Orders, Costumers, Recall, User
from utils.pagination import pagination


def kechagilar_def(page, limit, user, driver_id, db):
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

    rejadagilar_count = db.query(Recall).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'on'
    ).order_by(Recall.recall_date.desc(), Recall.recall_time.desc()).count()

    data['rejadagilar_count'] = rejadagilar_count

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


def rejadagilar_def(page, limit, user, operator_id, db):
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    six_months_ago = now - timedelta(days=180)

    rejadagilar = db.query(Recall).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'on'
    ).order_by(Recall.recall_date.desc(), Recall.recall_time.desc())
    if operator_id:
        rejadagilar = rejadagilar.filter(Recall.operator_id == operator_id)

    qizil_count = rejadagilar.filter(Recall.recall_date < now.date()).count()
    sariq_count = rejadagilar.filter(Recall.recall_date == now.date()).count()
    yashil_count = rejadagilar.filter(Recall.recall_date > now.date()).count()

    rejadagilar_count = rejadagilar.count()

    orders = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id == 0,
        Orders.order_status == 'topshirildi',
        Orders.order_date > six_months_ago
    )
    operator_count = db.query(Recall, Recall.operator_id,
                              func.count(Recall.operator_id).label('operator_count')).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'on'
    ).group_by(Recall.operator_id)

    yesterday_count = orders.count()
    data = pagination(rejadagilar, page, limit)
    data['yesterday_count'] = yesterday_count
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
    data['rejadagilar_count'] = rejadagilar_count
    data['qizil_count'] = qizil_count
    data['sariq_count'] = sariq_count
    data['yashil_count'] = yashil_count

    data['operators'] = operator_count.all()

    return data


def six_month_def(page, limit, user, driver_id, db):
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    six_months_ago = now - timedelta(days=180)
    six_month_orders = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id2 == 0,
        Orders.order_date < six_months_ago
    ).order_by(
        func.max(Orders.top_sana)
    ).group_by(Orders.costumer_id)
    orders = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.order_date > six_months_ago
    )
    driver_order_count = db.query(
        Orders,
        func.count(Orders.order_id).label('driver_order_count')).join(Orders.f_driver).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id2 == 0,
        Orders.order_date < six_months_ago,
    ).group_by(Orders.finish_driver).order_by(func.max(Orders.top_sana))
    if driver_id:
        six_month_orders = six_month_orders.filter(Orders.finish_driver == driver_id)

    yesterday_count = orders.filter(Orders.order_status == 'topshirildi', Orders.last_operator_id == 0).count()
    data = pagination(six_month_orders, page, limit)
    data['yesterday_count'] = yesterday_count
    six_month_count = six_month_orders.count()
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

    rejadagilar_count = db.query(Recall).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'on'
    ).order_by(Recall.recall_date.desc(), Recall.recall_time.desc()).count()

    data['rejadagilar_count'] = rejadagilar_count

    data['drivers'] = driver_order_count.group_by(Orders.finish_driver).all()

    return data


def calling_def(page, limit, user, db):
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    six_months_ago = now - timedelta(days=180)
    current_year = now.year
    orders_count1 = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        func.extract('year', Orders.top_sana) == current_year
    ).all()

    costumers_count = db.query(Costumers).filter(
        Costumers.costumers_filial_id == user.filial_id)
    costumers_id = []
    for item in orders_count1:
        costumers_id.append(item.costumer_id)
    calling = costumers_count.filter(Costumers.id.notin_(costumers_id))

    rejadagilar = db.query(Recall).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'on'
    ).order_by(Recall.recall_date.desc(), Recall.recall_time.desc())

    rejadagilar_count = rejadagilar.count()

    orders = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id == 0,
        Orders.order_status == 'topshirildi',
        Orders.order_date > six_months_ago
    )

    yesterday_count = orders.count()
    data = pagination(calling, page, limit)
    data['yesterday_count'] = yesterday_count
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

    data['calling'] = calling.count()
    data['rejadagilar_count'] = rejadagilar_count

    return data


def all_operators(page, limit, user, db):
    users = db.query(User).filter(User.filial_id == user.filial_id, User.status == 10)

    return pagination(users, page, limit)


def call_report_def(search, page, limit, user, operator_id, dan, gacha, db):
    call_reports = db.query(Recall).join(Recall.costumer).filter(
        Recall.recall_filial_id == user.filial_id,
        Recall.recall_status == 'off'
    ).order_by(Recall.recall_date.desc(), Recall.recall_time.desc())
    if dan:
        dan_date = datetime.combine(dan, datetime.min.time())
        call_reports = call_reports.filter(Recall.recall_date >= dan_date)
    if gacha:
        gacha_date = datetime.combine(gacha, datetime.max.time())
        call_reports = call_reports.filter(Recall.recall_date <= gacha_date)
    if search:
        search_formatted = "%{}%".format(search)
        call_reports = call_reports.filter(
            Recall.izoh.like(search_formatted) | Recall.recall_costumer_phone.like(search_formatted)
        )
    if operator_id:
        call_reports = call_reports.filter(Recall.operator_id == operator_id)

    data = pagination(call_reports, page, limit)
    return data


def recalling_def(search, q_natija, page, limit, user, last_operator_id, dan, gacha, db):
    orders = db.query(Orders).join(Orders.last_operator).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id > 0
    )
    if dan:
        dan_date = datetime.combine(dan, datetime.min.time())
        orders = orders.filter(Orders.talk_date >= dan_date)
    if gacha:
        gacha_date = datetime.combine(gacha, datetime.max.time())
        orders = orders.filter(Orders.talk_date <= gacha_date)
    if last_operator_id:
        orders = orders.filter(Orders.last_operator_id == last_operator_id)

    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(
            Orders.nomer.like(search_formatted) | Orders.costumer_id.like(search_formatted) |
            Orders.last_izoh.like(search_formatted)
        )

    if q_natija:
        orders = orders.filter(Orders.talk_type == q_natija.value)

    data = pagination(orders, page, limit)
    return data


def six_month_call_report_def(search, q_natija, page, limit, user, last_operator_id2, dan, gacha, db):
    orders = db.query(Orders).join(Orders.last_operator2).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.last_operator_id2 > 0
    )
    if dan:
        dan_date = datetime.combine(dan, datetime.min.time())
        orders = orders.filter(Orders.talk_date >= dan_date)
    if gacha:
        gacha_date = datetime.combine(gacha, datetime.max.time())
        orders = orders.filter(Orders.talk_date <= gacha_date)
    if last_operator_id2:
        orders = orders.filter(Orders.last_operator_id2 == last_operator_id2)

    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(
            Orders.nomer.like(search_formatted) | Orders.costumer_id.like(search_formatted) |
            Orders.last_izoh.like(search_formatted)
        )

    if q_natija:
        orders = orders.filter(Orders.talk_type == q_natija.value)

    data = pagination(orders, page, limit)
    return data
