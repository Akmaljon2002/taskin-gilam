from datetime import datetime
from math import floor
import pytz
from fastapi import HTTPException
from sqlalchemy import or_, func
from functions.buyurtma import select_all_buyurtma_with_status
from functions.orders import one_order
from functions.washing import clean_with_status_and_product, clean_with_status_and_product_sum
from models.models import User, Orders, Clean, NasiyaBelgilash, Mijoz_kirim, Nasiya
from schemas.washing import CleanStatus
from utils.pagination import save_in_db, pagination


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


def order_topshirish(order_id, filial_id, user, tolov_turi, summa, db):
    order = one_order(order_id, db)
    if not order:
        raise HTTPException(status_code=400, detail="Order not found!")
    clean = db.query(Clean).filter(Clean.order_id == order_id, Clean.clean_filial_id == filial_id,
                                   Clean.clean_status.in_([CleanStatus.QAYTA_QADOQLANDI.value]))
    qayta_yuv = db.query(Clean).filter(Clean.order_id == order_id, Clean.clean_status.in_([
        CleanStatus.QAYTA_YUVISH.value, CleanStatus.YUVILMOQDA.value]))
    qayta_qad = db.query(Clean).filter(Clean.order_id == order_id, Clean.clean_status.in_(
        [CleanStatus.QURIDI.value, CleanStatus.QAYTA_QURIDI.value]))

    nasiya_belgilas = db.query(NasiyaBelgilash).filter(NasiyaBelgilash.filial_id == filial_id).first()
    # if clean.count() == 0:
    #     raise HTTPException(status_code=400, detail="Clean hammasi tayyor!")

    buyurtma = select_all_buyurtma_with_status(db, order.order_id)
    total_sum = 0
    total_absolute_cost = float(0)
    total_count = 0
    order = None
    for item in buyurtma:
        # Clean larni chaqirib olish
        cleans = clean_with_status_and_product(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ])

        # Clean larni jami summasini chaqirib olish
        cleans_sum = clean_with_status_and_product_sum(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ])
        total_absolute_cost += float(cleans_sum)

        # Buyurtmani jami summasini olish
        total_sum += clean_with_status_and_product_sum(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ], reclean_place=True)

        # Burtma sonini hisoblash
        total_count += len(cleans)

        # Order-ni list tashqarisida chiqaramiz chunki u bitta
        order = item.order

    # Buyurtma uchun skida ni hisoblash
    total_with_discount_cost = 0

    if order.own == 0:
        total_with_discount_cost = float(total_sum)
        skidka = float(order.order_skidka_sum) + (total_with_discount_cost * float(order.order_skidka_foiz) / 100)
        if skidka <= total_with_discount_cost:
            total_with_discount_cost -= skidka
        else:
            total_with_discount_cost = 0
        discount_for_own = 100
    else:
        total_with_discount_cost = float(total_sum)
        if total_with_discount_cost > 0:
            discount_for_own = total_with_discount_cost / float(total_absolute_cost) * 100
        else:
            discount_for_own = 100

    # Yakuniy summa
    tolov_summa = total_with_discount_cost - order.avans

    if nasiya_belgilas:
        if nasiya_belgilas.foiz == 0:
            tsh_foiz = 1
        else:
            tsh_foiz = nasiya_belgilas.foiz
        tsh_sum = nasiya_belgilas.summa
    else:
        tsh_foiz = 1
        tsh_sum = 0
    tsh_foiz1 = 0
    if tsh_foiz:
        tsh_foiz1 = tsh_foiz / 100
    tushib_berish = tolov_summa - (total_absolute_cost * tsh_foiz1) - tsh_sum

    if tolov_summa < 0:
        chegirma_summa = abs(tolov_summa)
        tolov_summa = 0
    else:
        chegirma_summa = 0
        tolov_summa = floor(tolov_summa)

    # summalarni yaxlitlash
    tushib_berish = floor(tushib_berish)

    # buyurtmaning jami qiymatini hisoblash
    clean_sum = db.query(func.sum(Clean.clean_narx)).filter(Clean.order_id == order_id,
                                                            Clean.clean_filial_id == filial_id).scalar()
    order.order_price = clean_sum

    eski_last_price = order.order_last_price

    order_last_price = summa

    #pulni hamma qabul qilishdagi summasini o`sha  summani + 30% dan ko`p summasini kiritib bilmasin
    if order_last_price > (tolov_summa + tolov_summa / 2) or order_last_price < (tolov_summa / 2):
        raise HTTPException(status_code=400, detail="Summa noto`g`ri kiritildi!")

    if qayta_yuv.count() > 0 or qayta_qad.count() > 0:
        if qayta_yuv.count() > 0:
            order.order_status = 'qayta yuvish'
        elif qayta_qad.count() > 0 and qayta_yuv.count() > 0:
            order.order_status = 'qayta qadoqlash'
    else:
        order.order_status = 'topshirildi'

    order.order_skidka_foiz = 0
    order.order_skidka_sum = 0

    for item in clean.all():
        item.clean_status = 'topshirildi'
        item.top_sana = datetime.now(pytz.timezone('Asia/Tashkent'))
        item.top_user = user.id

    if order_last_price > 0:
        if tolov_turi == 'naqt':
            user.balance +=  order_last_price
        else:
            if tolov_turi == "Terminal-bank":
                user.plastik += order_last_price
            elif tolov_turi == "click":
                user.click += order_last_price

        kirim = Mijoz_kirim(
            summa=order_last_price,
            tolov_turi=tolov_turi,
            order_id=order_id,
            costumer_id=order.costumer_id,
            date=datetime.now(pytz.timezone('Asia/Tashkent')),
            status="olindi",
            user_id=user.id,
            filial_id=user.filial_id,
            updated_at="0000-00-00 00:00:00"
        )
        save_in_db(db, kirim)

    order.top_sana = datetime.now(pytz.timezone('Asia/Tashkent'))
    order.order_price_status = user.role
    order.finish_driver = user.id

    if order_last_price < tushib_berish:
        nasiya = Nasiya(
            summa=tolov_summa - order_last_price,
            nasiya=tolov_summa - order_last_price,
            nasiyachi_id=order.costumer_id,
            order_id=order_id,
            ber_date=datetime.now(pytz.timezone('Asia/Tashkent')),
            status=0,
            filial_id=user.filial_id,
            user_id=user.id,
            date=datetime.now(pytz.timezone('Asia/Tashkent')),
            updated_at="0000-00-00 00:00:00"
        )
        save_in_db(db, nasiya)
    order.order_last_price += order_last_price

    db.commit()
    return True


def ombordan_tartib_all(page, limit, filial_id, db):
    orders = db.query(Orders).filter(Orders.order_filial_id == filial_id, Orders.order_status == "ombor")
    return pagination(orders, page, limit)






