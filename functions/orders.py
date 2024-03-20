from datetime import datetime
from typing import Union
import pytz
from fastapi import HTTPException
from sqlalchemy import or_, desc, asc
from sqlalchemy.orm import joinedload, defer, load_only
from starlette import status
from models.models import Orders, Clean, Costumers, Buyurtma, User
from schemas.orders import OrderStatus
from schemas.washing import CleanStatus
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


def update_order(db, id: int, data: dict):
    order = db.query(Orders).filter(Orders.order_id == id).update(data)
    db.commit()
    return order


def order_get(page, limit, db, filial_id: int, status: list = None):
    """
    Barcha buyurtmalarni chaqirib olamiz user filiali bo'yicha va status bo'yicha
    """
    orders = db.query(Orders).options(joinedload(Orders.costumer)).order_by(desc(Orders.topshir_sana))
    if not status:
        orders = orders.filter(
            Orders.order_filial_id == filial_id,
        )
    else:
        orders = orders.join(Clean).filter(
            Clean.clean_status.in_(status)
        )
    return pagination(orders, page, limit)


def order_first(db, id: int, filial_id: int, joinload: bool = True, operator_old: bool = False):
    order = db.query(Orders).filter(Orders.order_id == id, Orders.order_filial_id == filial_id)
    if joinload:
        # Shunga qilishiga to'g'ri keldi. Bundan ham yaxshi yechilar bor albatta
        if operator_old:
            order = order.options(joinedload(Orders.operator), joinedload(Orders.costumer))
        else:
            order = order.options(joinedload(Orders.costumer))

    order = order.first()

    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu id bo'yicha ma'lumot topilmadi")

    return order


def order_filter_fililal_and_status_and_order_driver_count(db, filial_id: int, status: list, current_user: User = None,
                                                           saygak_id: int = None):
    query = db.query(Orders).filter(Orders.order_filial_id == filial_id, Orders.order_status.in_(status))

    # roli transport bo'lsa o'zini buyurtmalari chaqiriladi
    if current_user and current_user.role == "transport":
        query = query.filter(Orders.order_driver == current_user.id)

    # Saygak hodim bo'lsa
    if saygak_id:
        query = query.filter(Orders.saygak_id == saygak_id)
    else:
        query = query.filter(Orders.saygak_id == 0)
    query = query.count()

    return query


def order_tartiblanmagan_tartiblangan_haydovchilar_get(db, filial_id: int, status: list = None,
                                                       tartiblangan: bool = False):
    ordes_user = db.query(Orders) \
        .filter(Orders.order_filial_id == filial_id, Orders.order_status.in_(status)) \
        .options(joinedload(Orders.driver)).group_by(Orders.order_driver)

    # Tartiblangan bo'lsa nomer yoziladi tartiblanmagan bo'lsa nomer yozilmaydi (0)
    if tartiblangan:
        ordes_user = ordes_user.filter(Orders.tartib_raqam > 0)
    else:
        ordes_user = ordes_user.filter(Orders.tartib_raqam == 0)

    # Tartiblangan bo'lsa nomer yoziladi tartiblanmagan bo'lsa nomer yozilmaydi (0)
    if tartiblangan:
        ordes_user = ordes_user.filter(Orders.tartib_raqam > 0)
    else:
        ordes_user = ordes_user.filter(Orders.tartib_raqam == 0)

    ordes_user = ordes_user.all()

    def count():
        query = db.query(Orders).filter(Orders.order_driver == item.order_driver, Orders.order_status.in_(status))

        if tartiblangan:
            query = query.filter(Orders.tartib_raqam > 0)
        else:
            query = query.filter(Orders.tartib_raqam == 0)

        return query.count()

    data = []
    for item in ordes_user:
        data.append({
            'id': item.driver.id,
            'name': item.driver.fullname,
            'count': count()
        })

    return data


def order_tartiblanmagan_tartiblangan_get(db, page: int, limit: int, filial_id: int, status: list = None,
                                          tartiblangan: bool = False,
                                          joinedload_table: bool = True, own: bool = False, joyida: bool = False,
                                          count: bool = False, filter: Union[str, int] = None):
    '''Tayyor buyurtmalarni chaqirib olish
        * filial_id - fililyanlning id-si
        * status - Chaqirilishi kerak bo'lgan statusdagi buyurtmalar
        * tartiblangan - Tayyor buyurtmalar 2 ga bo'linadi tartiblangan va tartiblanmagan shularni qay biriligini tanlash kerak
        * joinedload_table - Bizga bo'glangan bazalarni chaqirishi yoki chaqirmasligni belgilab beradi
        * own - Buyurtmlarni mijoz o'zi olib ketadiganlarini ajiratib beradi
        * joyida - Joyida yuviladigan buyurtmalarni ajiratib beradi
        * count - Chaqririlgan ma'lumotlarni count-ni qaytaradi
        * filter - Buyurtmalarni own, joyida va transport hodim id orqali ularni buyurtmalarini chiqarish
    '''

    query = db.query(Orders).join(Orders.cleans).filter(
        Orders.order_filial_id == filial_id,
        Orders.order_status.in_(status)
    )

    # Mijoz o'zi olip ketadigan buyurtmalar
    if own or (filter and filter == 'own'):
        query = query.filter(Orders.own == 1)

    # Joyida yuviladigan buyurtmalar
    if joyida or (filter and filter == 'joyida'):
        query = query.filter(Orders.own == 1)

    # Filter raqam jo'natsak ham str kelyapti shuni raqmga par qilvolamiz
    if filter:
        try:
            filter = int(filter)
        except ValueError as err:
            pass

        # Haydovchi buyurtmalari
        if type(filter) == int:
            query = query.filter(Orders.order_driver == filter)

    # Tartiblangan bo'lsa nomer yoziladi tartiblanmagan bo'lsa nomer yozilmaydi (0)
    if tartiblangan:
        query = query.filter(Orders.tartib_raqam > 0).order_by(asc(Orders.tartib_raqam))
    else:
        query = query.filter(Orders.tartib_raqam == 0).order_by(asc(Orders.topshir_sana))

    if joinedload_table:
        query = query.options(
            joinedload(Orders.operator),
            joinedload(Orders.costumer),
            joinedload(Orders.cleans).joinedload(Clean.xizmat),
        )

    # Bazida count-ni ham olishga to'g'ri keladi ;)
    if count:
        query = query.all()
        query = len(query)
        return query
    else:
        query = query

    return pagination(query, page, limit)


def omborga_otkazish(order_id, filial_id, user_id, db):
    order = db.query(Orders).filter(Orders.order_id == order_id, Orders.order_filial_id == filial_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    order.order_status = "ombor"
    order.ombor_user = user_id
    db.commit()
    return True


def order_ombordan_tayyorga(order_id, filial_id, db):
    order = db.query(Orders).filter(Orders.order_id == order_id, Orders.order_filial_id == filial_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order topilmadi!")
    cleans = db.query(Clean).filter(Clean.order_id == order_id,
                                    Clean.clean_status == CleanStatus.QAYTA_QADOQLANDI.value).count()
    if cleans > 0:
        order.order_status = OrderStatus.QAYTA_QADOQLANDI.value
    else:
        order.order_status = OrderStatus.QADOQLANDI.value
    order.ombor_user = 0
    db.commit()
    return True


def currently_def(search, status_clean, muddat, page, limit, user, db):
    if status_clean:
        search_formatted = "%{}%".format(status_clean.value)
        orders = db.query(Orders).filter(Orders.order_filial_id == user.filial_id).join(Orders.cleans).filter(
            Clean.clean_status.like(search_formatted)
        )
    else:
        orders = db.query(Orders).join(Clean).filter(Orders.order_filial_id == user.filial_id)

    if muddat:
        now_date = datetime.now(pytz.timezone('Asia/Tashkent')).date()
        if muddat.value == "qizil":
            orders = orders.filter(Orders.topshir_sana < now_date)
        elif muddat.value == "sariq":
            orders = orders.filter(Orders.topshir_sana == now_date)
        else:
            orders = orders.filter(Orders.topshir_sana > now_date)

    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.join(Costumers).filter(
            Orders.nomer.like(search_formatted) | Costumers.costumer_phone_1.like(search_formatted) |
            Costumers.costumer_phone_2.like(search_formatted) | Costumers.costumer_phone_3.like(search_formatted))

    return pagination(orders, page, limit)
