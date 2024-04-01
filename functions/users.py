from datetime import datetime
from operator import or_

import pytz
from fastapi import HTTPException
from models.models import User
from routers.auth import hash_password
from utils.pagination import pagination, save_in_db


def one_user(id, branch_id, db):
    user = db.query(User).filter(User.id == id)
    if branch_id is not None:
        user = user.filter(User.branch_id == branch_id)
    return user.first()


def all_users(search, status, role, page, limit, user, db):
    users = db.query(User).filter(User.filial_id == user.filial_id)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(User.username.like(search_formatted) | User.fullname.like(search_formatted) |
                             User.phone.like(search_formatted) | User.phone2.like(search_formatted) |
                             User.user_moi_zvonki_address.like(search_formatted))
    if status is not None:
        users = users.filter(User.status == status)
    if role:
        users = users.filter(User.role == role)
    return pagination(users, page, limit)


async def create_user(form, user, db):
    check_user = db.query(User).filter(User.username == form.username, User.filial_id == user.filial_id).first()
    chech_phone = db.query(User).filter(User.phone == form.phone).first()
    if check_user:
        raise HTTPException(status_code=403, detail="User already exists!")
    if chech_phone:
        raise HTTPException(status_code=400, detail="Phone already exists!")
    new_user = User(
        username=form.username,
        fullname=form.fullname,
        phone=form.phone,
        phone2=form.phone2,
        password_hash=hash_password(form.password_hash),
        role=form.role,
        filial_id=user.filial_id,
        oylik=form.oylik,
        kpi=form.kpi,
        ozroq_kpi=form.ozroq_kpi,
        maosh=form.maosh,
        moi_zvonki_user_name=form.moi_zvonki_user_name,
        user_moi_zvonki_address=form.user_moi_zvonki_address,
        user_moi_zvonki_api=form.user_moi_zvonki_api,
        status=10,
        zayavka_limit=form.zayavka_limit,
        topshirish_limit=form.topshirish_limit,
        skald_limit=form.skald_limit,
        zakaz_status=form.zakaz_status,
        created_at=datetime.now(pytz.timezone('Asia/Tashkent')).timestamp(),
        updated_at=0

    )
    save_in_db(db, new_user)
    return new_user


async def update_user(form, the_user, db):
    user = db.query(User).filter_by(id=form.user_id, filial_id=the_user.filial_id)
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found!")
    if user.first().phone != form.phone:
        check_phone = db.query(User).filter(User.phone == form.phone,
                                            User.filial_id == the_user.filial_id).first()
        if check_phone:
            raise HTTPException(status_code=400, detail="Phone already exists!")
    if form.password_hash:
        user.password_hash = hash_password(form.password_hash)

    user.update({
        User.username: form.username,
        User.fullname: form.fullname,
        User.role: form.role,
        User.phone: form.phone,
        User.phone2: form.phone2,
        User.maosh: form.maosh,
    })
    db.commit()
    return True
