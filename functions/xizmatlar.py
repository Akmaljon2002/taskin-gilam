from datetime import datetime

import pytz
from fastapi import HTTPException
from starlette import status
from models.models import Xizmatlar
from schemas.xizmatlar import XizmatStatus
from utils.pagination import pagination, save_in_db


def all_xizmatlar(filial_id, db):
    xizmatlar = db.query(Xizmatlar).filter(Xizmatlar.filial_id == filial_id, Xizmatlar.status == "active")
    xizmatlar = xizmatlar.order_by(Xizmatlar.xizmat_turi.asc())
    return xizmatlar.all()


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


def create_xizmat(form, user, db):
    new_xizmat_db = Xizmatlar(
        xizmat_turi=form.xizmat_turi,
        olchov=form.olchov.value,
        status=form.status.value,
        operator_kpi_line=form.operator_kpi_line,
        narx=form.narx,
        min_narx=form.min_narx,
        discount_for_own=form.discount_for_own,
        saygak_narx=form.saygak_narx,
        filial_id=user.filial_id,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')),
        updated_at="0000-00-00 00:00:00"

    )
    save_in_db(db, new_xizmat_db)
    return new_xizmat_db


def update_xizmat(form, user, db):
    xizmat = one_xizmat(form.xizmat_id, user.filial_id, db)
    if xizmat is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli xizmat mavjud emas")

    xizmat.xizmat_turi = form.xizmat_turi,
    xizmat.olchov = form.olchov.value,
    xizmat.status = form.status.value,
    xizmat.operator_kpi_line = form.operator_kpi_line,
    xizmat.narx = form.narx,
    xizmat.min_narx = form.min_narx,
    xizmat.discount_for_own = form.discount_for_own,
    xizmat.saygak_narx = form.saygak_narx,
    db.commit()

    return True
