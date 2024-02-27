from datetime import datetime
import pytz
from fastapi import HTTPException
from sqlalchemy import or_, desc
from sqlalchemy.orm import joinedload, defer, load_only
from models.models import Orders, Clean, Costumers, Buyurtma
from utils.pagination import pagination


def all_orders(search, page, limit, db):
    orders = db.query(Orders).options(
        load_only("order_id", "operator_id", "izoh", "izoh2", "order_price", "order_last_price", "order_driver",
                  "finish_driver", "order_date", "olibk_sana", "top_sana", "ch_sum", "ch_foiz", "own"),
        joinedload("cleans").options(load_only("clean_hajm", "gilam_eni", "gilam_boyi", "clean_narx", "narx", "user_id",
                                               "joy", "qad_user")))
    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(
            Orders.nomer.like(search_formatted) | Orders.saygak_id.like(search_formatted))
    return pagination(orders, page, limit)


def one_order(order_id, db):
    return db.query(Orders).filter(Orders.order_id == order_id).options(
        load_only("order_id", "operator_id", "izoh", "izoh2", "order_price", "order_last_price", "order_driver",
                  "finish_driver", "order_date", "olibk_sana", "top_sana", "ch_sum", "ch_foiz", "own"),
        joinedload("cleans").options(load_only("clean_hajm", "gilam_eni", "gilam_boyi", "clean_narx", "narx", "user_id",
                                               "joy", "qad_user"))).first()


def orders_to_drivers(search, page, limit, user_id, status, db):
    orders = db.query(Orders).options(
        joinedload("driver"),
        joinedload("operator").options(defer("password_hash"), defer("api_token"), defer("auth_key")),
        joinedload("costumer").subqueryload("millat").options(load_only("name"))
    )
    if status == "keltirish":
        orders = orders.filter(
            Orders.order_status == "keltirish", or_(Orders.order_driver == "hamma", Orders.order_driver == user_id))
    else:
        orders = orders.filter(
            Orders.order_status == "qabul qilindi", Orders.order_driver == user_id
        ).order_by(desc(Orders.order_id))
    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(
            Orders.nomer.like(search_formatted) | Orders.saygak_id.like(search_formatted))
    return pagination(orders, page, limit)


def order_to_drivers(order_id, db):
    order = db.query(Orders).filter(Orders.order_id == order_id).options(
        joinedload("driver"),
        joinedload("operator").options(defer("password_hash"), defer("api_token"), defer("auth_key")),
        joinedload("costumer").subqueryload("millat").options(load_only("name"))
    ).first()
    return order


def recleans(search, page, limit, user_id, db):
    cleans = db.query(Clean).filter(Clean.reclean_place == 3,
                                    or_(Clean.reclean_driver == 0, Clean.reclean_driver == user_id)).options(
        joinedload("order").subqueryload('operator').options(defer("password_hash"), defer("auth_key"),
                                                             defer("api_token")),
        joinedload("driver"), joinedload("costumer").subqueryload("millat").options(load_only("name"))
    )
    if search:
        search_formatted = "%{}%".format(search)
        cleans = cleans.filter(
            Orders.nomer.like(search_formatted) | Orders.saygak_id.like(search_formatted))
    cleans = cleans.group_by("order_id", "reclean_driver")
    return pagination(cleans, page, limit)


def reclean(clean_id, db):
    clean = db.query(Clean).filter(Clean.id == clean_id).options(
        joinedload("order").subqueryload('operator').options(defer("password_hash"), defer("auth_key"),
                                                             defer("api_token")),
        joinedload("driver"), joinedload("costumer").subqueryload("millat").options(load_only("name"))).first()
    return clean


def accept_order(form, user_id, filial_id, db):
    order = db.query(Orders).filter(Orders.order_id == form.order_id, Orders.order_filial_id == filial_id,
                                    Orders.order_status == "keltirish").first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi yoki qabul qilingan!")
    costumer = db.query(Costumers).filter(Costumers.id == order.costumer_id).first()

    order.order_driver = user_id
    order.finish_driver = 0
    order.order_price = 0
    order.order_last_price = 0
    order.tartib_raqam = 0
    order.order_price_status = "yoq"
    order.order_status = "qabul qilindi"
    order.olibk_sana = form.topshir_sana

    if len(form.xizmatlar) == 0:
        raise HTTPException(status_code=400, detail="Bitta bo`lsa ham mahsulot kiriting!")
    for xizmat in form.xizmatlar:
        if xizmat.quantity > 0:
            buyurtma = Buyurtma(
                x_id=xizmat.xizmat_id,
                status=1,
                value=xizmat.quantity,
                filial_id=filial_id,
                order_id=form.order_id,
                created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
                updated_at="0000-00-00 00:00:00"
            )
            db.add(buyurtma)
    costumer.costumers_filial_id = filial_id
    costumer.costumer_status = "kutish"
    db.commit()
    return True


def edit_order_driver(order_id, driver_id, filial_id, db):
    order = db.query(Orders).filter(Orders.order_id == order_id, Orders.order_filial_id == filial_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    if driver_id == 0:
        driver_id = "hamma"
    order.order_driver = driver_id
    db.commit()
    return True


def cancel_order(form, filial_id, db):
    order = db.query(Orders).filter(Orders.order_id == form.order_id, Orders.order_filial_id == filial_id).first()
    costumer = db.query(Costumers).filter(Costumers.id == order.costumer_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    order.order_status = "bekor qilindi"
    order.izoh = form.izoh
    costumer.costumer_status = "kutish"
    db.commit()
    return True


def called_order(order_id, filial_id, db):
    order = db.query(Orders).filter(Orders.order_id == order_id, Orders.order_filial_id == filial_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    order.called = 1
    db.commit()
    return True
