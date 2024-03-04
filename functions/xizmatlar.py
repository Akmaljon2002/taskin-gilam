from datetime import datetime
import pytz
from fastapi import HTTPException
from starlette import status

from functions.users import one_user
from models.models import Xizmatlar
from schemas.xizmatlar import XizmatStatus
from utils.pagination import pagination, save_in_db, is_date_valid


def all_xizmatlar(search, page, limit, filial_id, db):
    xizmatlar = db.query(Xizmatlar).filter(Xizmatlar.filial_id == filial_id, Xizmatlar.status == "active")
    if search:
        search_formatted = "%{}%".format(search)
        xizmatlar = xizmatlar.filter(
            Xizmatlar.xizmat_turi.like(search_formatted))
    xizmatlar = xizmatlar.order_by(Xizmatlar.xizmat_turi.asc())
    return pagination(xizmatlar, page, limit)


def one_xizmat(id, filial_id, db):
    return db.query(Xizmatlar).filter(Xizmatlar.xizmat_id == id,
                                      Xizmatlar.filial_id == filial_id, Xizmatlar.status == "active").first()


def select_xizmat_firsrt(db, id: int, filial_id: int):
    data = db.query(Xizmatlar).filter(
        Xizmatlar.xizmat_id == id,
        Xizmatlar.filial_id == filial_id,
        Xizmatlar.status == XizmatStatus.ACTIVE.value
    ).first()

    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bu id bo'yicha ma'lumot topilmadi")

    return data


# def create_xizmat(form, user_id, db):
#     if not is_date_valid(form.deadline):
#         raise HTTPException(status_code=400, detail="You entered the wrong deadline!")
#     if not one_user(form.admin_id, 0, db):
#         raise HTTPException(status_code=400, detail="Admin_id not found!")
#     new_xizmat_db = Xizmatlar(
#         name=form.name,
#         address=form.address,
#         comment=form.comment,
#         user_id=user_id,
#         admin_id=form.admin_id,
#         deadline=form.deadline,
#         status=form.status,
#         date=datetime.now(pytz.timezone('Asia/Tashkent'))
#
#     )
#     save_in_db(db, new_xizmat_db)
#     return new_xizmat_db
#
#
# def update_xizmat(form, db):
#     if not is_date_valid(form.deadline):
#         raise HTTPException(status_code=400, detail="You entered the wrong deadline!")
#     if one_xizmat(form.id, db) is None:
#         raise HTTPException(status_code=400, detail="Bunday id raqamli mijoz mavjud emas")
#     if not one_user(form.admin_id, 0, db):
#         raise HTTPException(status_code=400, detail="Admin_id not found!")
#
#     db.query(Xizmatlar).filter(Xizmatlar.id == form.id).update({
#         Xizmatlar.name: form.name,
#         Xizmatlar.address: form.address,
#         Xizmatlar.admin_id: form.admin_id,
#         Xizmatlar.comment: form.comment,
#         Xizmatlar.deadline: form.deadline,
#         Xizmatlar.status: form.status,
#
#     })
#     db.commit()
#
#     return True
