from datetime import datetime

import pytz
from sqlalchemy import or_, func
from models.models import User, Kirim, Chiqim
from utils.pagination import pagination


def kirimlar_def(page, limit, user, db):
    hodimlar = db.query(User).filter(User.filial_id == user.filial_id, or_(User.click > 0, User.balance > 0,
                                     User.plastik > 0))
    return pagination(hodimlar, page, limit)


def kirim_olindi(user, form, db):
    hodim = db.query(User).filter(User.id == form.user_id, User.filial_id == user.filial_id).first()
    now = datetime.now(pytz.timezone('Asia/Tashkent'))
    kirim_new = Kirim(
        kirim_filial_id=user.filial_id,
        kirim_user_id=form.user_id,
        user_fullname="-",
        kassachi_fullname="-",
        kassachi_id=user.id,
        tolov_turi="naqd",
        kirim_date=now,
        kirim_summ=form.kirim_summ,
        updated_at="0000-00-00 00:00:00"
    )

    chiqim_new = Chiqim(
        chiqim_filial_id=user.filial_id,
        chiqim_user_id=form.user_id,
        doimiy_izoh="kassa",
        chiqim_date=now,
        chiqim_summ=form.chiqim_summ,
        chiqim_firma=form.chiqim_firma,
        chiqim_shaxsiy=form.chiqim_shaxsiy,
        chiqim_izoh=form.chiqim_izoh,
        updated_at="0000-00-00 00:00:00"
    )
    if hodim.plastik > 0:
        kirim_new.kirim_summ = hodim.plastik
        kirim_new.tolov_turi = "Terminal-bank"
    if hodim.click > 0:
        kirim_new.kirim_summ = hodim.click
        kirim_new.tolov_turi = "click"

    if hodim.role == "saygak":
        hodim.balance -= kirim_new.kirim_summ
    else:
        hodim.balance = 0
        if form.chiqim_summ > 0 and form.chiqim_shaxsiy > 0:
            hodim.oylik -= form.chiqim_shaxsiy
    db.add(kirim_new)
    db.add(chiqim_new)
    db.commit()
    return True


def filter_uchun_hodimlar(user, db):
    hodimlar = db.query(User).filter(User.filial_id == user.filial_id, User.status == 10,
                                     User.role.in_(['admin', 'admin_filial', 'joyida_yuvish', 'transport', 'saygak']))
    return hodimlar.all()


def kassa_kirimlar_get_def(search, page, limit, user, date_s, kassachi_id, kassachi_top, db):
    sana = datetime.now(pytz.timezone('Asia/Tashkent')).date()
    if date_s:
        sana = date_s
    kirimlar = db.query(Kirim).filter(Kirim.kirim_filial_id == user.filial_id, func.date(Kirim.kirim_date) == sana)
    if search:
        search_formatted = "%{}%".format(search)
        kirimlar = kirimlar.filter(
            Kirim.kirim_summ.like(search_formatted) | Kirim.kirim_turi.like(search_formatted)
        )
    if kassachi_top:
        kirimlar = kirimlar.filter(Kirim.kirim_user_id == kassachi_top)
    if kassachi_id:
        kirimlar = kirimlar.filter(Kirim.kassachi_id == kassachi_id)
    return pagination(kirimlar, page, limit)
