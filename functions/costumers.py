from fastapi import HTTPException
from sqlalchemy.orm import joinedload, load_only

from models.models import Costumers, Mijoz_kirim, Nasiya
from routers.auth import hash_password
from utils.pagination import pagination


def all_costumers(search, page, limit, db):
    costumers = db.query(Costumers)
    if search:
        search_formatted = "%{}%".format(search)
        costumers = costumers.filter(
            Costumers.costumer_name.like(search_formatted) | Costumers.costumer_phone_1.like(search_formatted) |
            Costumers.costumer_phone_2.like(search_formatted) | Costumers.costumer_phone_3.like(search_formatted) |
            Costumers.manba.like(search_formatted) | Costumers.izoh.like(search_formatted) |
            Costumers.costumer_turi.like(search_formatted) | Costumers.costumer_addres.like(search_formatted))
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


def create_costumer(form, user_id, db):
    new_costumer = Costumers(
        costumer_name=form.costumer_name,
        costumer_phone_1=form.costumer_phone_1,
        costumer_phone_2=form.costumer_phone_2,
        costumer_addres=form.costumer_addres,
        manba=form.manba,
        costumer_status="kutish",
        user_id=user_id,
        costumer_turi=form.costumer_turi,
        izoh=form.izoh,
        millat_id=form.millat_id

    )
    db.add(new_costumer)
    db.commit()
    db.refresh(new_costumer)
    return new_costumer


async def update_costumer(form, db):
    costumer = db.query(Costumers).filter_by(id=form.costumer_id, is_active=True)
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
