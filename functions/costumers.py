import pytz
from fastapi import HTTPException
from sqlalchemy import asc
from sqlalchemy.orm import joinedload, load_only
from datetime import datetime
from models.models import Costumers, Mijoz_kirim, Nasiya, Recall, Orders, Xizmatlar, Chegirma
from schemas.costumers import TolovTuri
from utils.orders import order_nomer
from utils.pagination import pagination, save_in_db


def all_costumers(search, page, limit, db):
    costumers = db.query(Costumers)
    if search:
        search_formatted = "%{}%".format(search)
        costumers = costumers.filter(
            Costumers.costumer_name.like(search_formatted) | Costumers.costumer_phone_1.like(search_formatted) |
            Costumers.costumer_phone_2.like(search_formatted) | Costumers.costumer_phone_3.like(search_formatted) |
            Costumers.costumer_addres.like(search_formatted))
    return pagination(costumers, page, limit)


def history_costumer(search, page, limit, costumer_id, db):
    history = db.query(Mijoz_kirim).filter(Mijoz_kirim.costumer_id == costumer_id).options(
        load_only("summa", "tolov_turi", "date", "status"), joinedload("user").options(load_only("id", "fullname")),
        joinedload("order").options(load_only("order_id", "nomer")))
    if search:
        search_formatted = "%{}%".format(search)
        history = history.filter(
            Mijoz_kirim.costumer_id.like(search_formatted) | Mijoz_kirim.order_id.like(search_formatted) |
            Mijoz_kirim.user_id.like(search_formatted) | Mijoz_kirim.kassachi_id.like(search_formatted))
    return pagination(history, page, limit)


def nasiyalar(search, page, limit, costumer_id, db):
    nasiyalar = db.query(Nasiya).filter(Nasiya.nasiyachi_id == costumer_id).options(
        load_only("summa", "nasiya", "ber_date"), joinedload("order").options(load_only("nomer")))
    if search:
        search_formatted = "%{}%".format(search)
        nasiyalar = nasiyalar.filter(
            Nasiya.nasiyachi_id.like(search_formatted) | Nasiya.order_id.like(search_formatted) |
            Nasiya.user_id.like(search_formatted) | Nasiya.filial_id.like(search_formatted))
    return pagination(nasiyalar, page, limit)


def create_costumer_order(form, user_id, filial_id, db):
    phone_val = db.query(Costumers).filter(Costumers.costumer_phone_1 == f"+998{form.costumer_phone_1}").first()
    if phone_val:
        raise HTTPException(status_code=400, detail="Bunda telefon nomer oldin royhatdan o'tkazilgan!")
    if form.costumer_phone_2:
        form.costumer_phone_2 = f"+998{form.costumer_phone_2}"
    new_costumer = Costumers(
        costumers_filial_id=filial_id,
        costumer_name=form.costumer_name,
        costumer_phone_1=f"+998{form.costumer_phone_1}",
        costumer_phone_2=form.costumer_phone_2,
        costumer_addres=form.costumer_addres,
        manba=form.manba,
        costumer_status="kutish",
        user_id=user_id,
        costumer_turi=form.costumer_turi,
        izoh=form.izoh,
        millat_id=form.millat_id,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
        updated_at="0000-00-00 00:00:00"

    )
    save_in_db(db, new_costumer)
    if form.recall:
        new_recall = Recall(
            recall_filial_id=new_costumer.costumers_filial_id,
            recall_costumer_phone=form.costumer_phone_1,
            recall_date=form.recall.recall_date,
            recall_time=form.recall.recall_time,
            recall_status="on",
            izoh=form.recall.izoh,
            user_id=user_id,
            operator_id=user_id,
            created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
            updated_at="0000-00-00 00:00:00",
        )
        db.add(new_recall)

    if form.buyurtma:
        nomer = order_nomer(db)
        new_order = Orders(
            costumer_id=new_costumer.id,
            nomer=nomer,
            operator_id=user_id,
            order_filial_id=filial_id,
            order_date=datetime.now(pytz.timezone('Asia/Tashkent')),
            olibk_sana="0000-00-00 00:00:00",
            izoh=form.buyurtma_olish.izoh,
            order_driver=form.buyurtma_olish.order_driver,
            order_skidka_foiz=form.buyurtma_olish.order_skidka_foiz,
            order_skidka_sum=form.buyurtma_olish.order_skidka_sum,
            created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
            updated_at="0000-00-00 00:00:00",
        )
        new_costumer.costumer_status = "keltirish"
        save_in_db(db, new_order)
        for x_item in form.buyurtma_olish.xizmat:
            if 0 < x_item.chegirma_summa < x_item.summa:
                new_chegirma = Chegirma(
                    order_id=new_order.order_id,
                    xizmat_id=x_item.id,
                    summa=x_item.summa-x_item.chegirma_summa,
                    created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
                    updated_at="0000-00-00 00:00:00"
                )
                db.add(new_chegirma)

    db.commit()
    return True


def create_costumer(form, user_id, filial_id, db):
    phone_val = db.query(Costumers).filter(Costumers.costumer_phone_1 == f"+998{form.costumer_phone_1}").first()
    if phone_val:
        raise HTTPException(status_code=400, detail="Bunda telefon nomer oldin royhatdan o'tkazilgan!")
    if form.costumer_phone_2:
        form.costumer_phone_2 = f"+998{form.costumer_phone_2}"
    new_costumer = Costumers(
        costumers_filial_id=filial_id,
        costumer_name=form.costumer_name,
        costumer_phone_1=f"+998{form.costumer_phone_1}",
        costumer_phone_2=form.costumer_phone_2,
        costumer_addres=form.costumer_addres,
        manba=form.manba,
        costumer_status="keltirish",
        user_id=user_id,
        millat_id=form.millat_id,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
        updated_at="0000-00-00 00:00:00"

    )
    save_in_db(db, new_costumer)

    return True


async def update_costumer(form, db):
    costumer = db.query(Costumers).filter_by(id=form.id)
    if costumer.first() is None:
        raise HTTPException(status_code=404, detail="Costumer not found!")

    costumer.update({
        Costumers.costumer_name: form.costumer_name,
        Costumers.costumer_phone_1: form.costumer_phone_1,
        Costumers.costumer_phone_2: form.costumer_phone_2,
        Costumers.costumer_addres: form.costumer_addres,
        Costumers.manba: form.manba,
        Costumers.costumer_turi: form.costumer_turi,
        Costumers.izoh: form.izoh,
        Costumers.millat_id: form.millat_id
    })
    db.commit()
    return True


def nasiyachilar(filial_id, db):
    costumers = db.query(Costumers).filter(Costumers.costumers_filial_id == filial_id).all()
    nasiyachilar = []
    for item in costumers:
        nasiya = db.query(Nasiya).filter(Nasiya.filial_id == filial_id, Nasiya.nasiyachi_id == item.id,
                                         Nasiya.status.in_([0, 1])).first()
        if nasiya:
            nasiyachilar.append(item)
    return nasiyachilar


def nasiyalar_all(filter, page, limit, costumer_id, filial_id, db):
    nasiyalar = db.query(Nasiya).filter(Nasiya.filial_id == filial_id, Nasiya.status.in_([0, 1])).options(
        joinedload("nasiyachi"))
    if costumer_id:
        nasiyalar = nasiyalar.filter(Nasiya.nasiyachi_id == costumer_id)
    if filter:
        filter_formatted = "%{}%".format(filter)
        nasiyalar = nasiyalar.join(Costumers).filter(
            Nasiya.nasiyachi_id.like(filter_formatted) | Costumers.costumer_phone_1.like(filter_formatted) |
            Costumers.costumer_name.like(filter_formatted) | Nasiya.filial_id.like(filter_formatted))
    return pagination(nasiyalar.order_by(asc(Nasiya.ber_date)), page, limit)


def nasiya_olish(form, user, db):
    tolov_turi = form.tolov_turi.value
    ol_summa = form.ol_summa
    nasiya = db.query(Nasiya).filter(Nasiya.id == form.nasiya_id).first()
    if nasiya.summa < ol_summa:
        raise HTTPException(detail="Nasiya summadan katta summa kiritildi", status_code=400)
    nasiya.summa -= ol_summa
    if ol_summa>0:
        mijoz_kirim = Mijoz_kirim(
            summa=ol_summa,
            tolov_turi=tolov_turi,
            order_id=nasiya.order_id,
            costumer_id=nasiya.nasiyachi_id,
            date=datetime.now(pytz.timezone('Asia/Tashkent')),
            status="olindi",
            user_id=user.id,
            filial_id=user.filial_id,
            updated_at="0000-00-00 00:00:00"
        )
        save_in_db(db, mijoz_kirim)
        if tolov_turi == TolovTuri.Naqt.value:
            user.balance += ol_summa
        else:
            if tolov_turi == TolovTuri.Terminal_bank.value:
                user.plastik += ol_summa
            elif tolov_turi == TolovTuri.Click.value:
                user.click += ol_summa
        if nasiya.summa == 0:
            nasiya.status = 3
    db.commit()
    return True


def nasiya_kechish(nasiya_id, user, db):
    nasiya = db.query(Nasiya).filter(Nasiya.id == nasiya_id).first()
    nasiya.status = 4
    if nasiya.summa > 0:
        mijoz_kirim = Mijoz_kirim(
            summa=nasiya.summa,
            tolov_turi=TolovTuri.Naqt.value,
            order_id=nasiya.order_id,
            costumer_id=nasiya.nasiyachi_id,
            date=datetime.now(pytz.timezone('Asia/Tashkent')),
            status="kechildi",
            user_id=user.id,
            filial_id=user.filial_id,
            updated_at="0000-00-00 00:00:00"
        )
        save_in_db(db, mijoz_kirim)
    db.commit()
    return True


def nasiyalar_tasdiqlanmagan_all(page, limit, filial_id, db):
    nasiyalar = db.query(Nasiya).filter(Nasiya.filial_id == filial_id, Nasiya.status == 0).options(
        joinedload("nasiyachi"))
    return pagination(nasiyalar.order_by(asc(Nasiya.ber_date)), page, limit)


def nasiya_tasdiqlash(nasiya_id, ber_date, db):
    nasiya = db.query(Nasiya).filter(Nasiya.id == nasiya_id, Nasiya.status == 0).first()
    if not nasiya:
        raise HTTPException(status_code=400, detail="Nasiya not found!")
    nasiya.status = 1
    nasiya.ber_date = ber_date
    db.commit()
    return True


