from datetime import datetime
import pytz
from fastapi import HTTPException
from functions.users import one_user
from models.models import Filial
from utils.pagination import pagination, save_in_db, is_date_valid


def all_branches(search, page, limit, db):
    branches = db.query(Filial)
    if search:
        search_formatted = "%{}%".format(search)
        branches = branches.filter(
            Filial.filial_name.like(search_formatted))
    branches = branches.order_by(Filial.filial_name.asc())
    return pagination(branches, page, limit)


def one_branch(id, db):
    return db.query(Filial).filter(Filial.filial_id == id).first()


def create_branch(form, user_id, db):
    if not is_date_valid(form.deadline):
        raise HTTPException(status_code=400, detail="You entered the wrong deadline!")
    if not one_user(form.admin_id, 0, db):
        raise HTTPException(status_code=400, detail="Admin_id not found!")
    new_branch_db = Filial(
        name=form.name,
        address=form.address,
        comment=form.comment,
        user_id=user_id,
        admin_id=form.admin_id,
        deadline=form.deadline,
        status=form.status,
        date=datetime.now(pytz.timezone('Asia/Tashkent'))

    )
    save_in_db(db, new_branch_db)
    return new_branch_db


def update_branch(form, db):
    if not is_date_valid(form.deadline):
        raise HTTPException(status_code=400, detail="You entered the wrong deadline!")
    if one_branch(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli mijoz mavjud emas")
    if not one_user(form.admin_id, 0, db):
        raise HTTPException(status_code=400, detail="Admin_id not found!")

    db.query(Filial).filter(Filial.id == form.id).update({
        Filial.name: form.name,
        Filial.address: form.address,
        Filial.admin_id: form.admin_id,
        Filial.comment: form.comment,
        Filial.deadline: form.deadline,
        Filial.status: form.status,

    })
    db.commit()

    return True
