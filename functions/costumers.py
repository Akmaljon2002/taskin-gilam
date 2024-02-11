from fastapi import HTTPException
from models.models import Costumers
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


def create_costumer(form, user_id, db):
    new_costumer = Costumers(
        costumer_name=form.costumer_name,
        costumer_phone_1=form.costumer_phone_1,
        costumer_phone_2=form.costumer_phone_2,
        costumer_addres=form.costumer_addres,
        manba=form.manba,
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
        Costumers.costumername: form.costumername,
        Costumers.password: hash_password(form.password),
        Costumers.role: form.role,
        Costumers.is_active: form.is_active,
    })
    db.commit()
    return True
