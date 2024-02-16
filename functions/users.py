from fastapi import HTTPException
from models.models import User
from routers.auth import hash_password
from utils.pagination import pagination, save_in_db


def one_user(id, branch_id, db):
    user = db.query(User).filter(User.id == id)
    if branch_id is not None:
        user = user.filter(User.branch_id == branch_id)
    return user.first()


def all_users(search, status, role, page, limit, db):
    users = db.query(User)
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


async def create_user(form, db):
    check_user = db.query(User).filter_by(username=form.username).first()
    if check_user:
        raise HTTPException(status_code=403, detail="User already exists!")
    new_user = User(
        username=form.username,
        password=hash_password(form.password),
        role=form.role,
        is_active=form.is_active,

    )
    save_in_db(db, new_user)
    return new_user


async def update_user(form, db):
    user = db.query(User).filter_by(id=form.user_id, is_active=True)
    if user.first() is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user.update({
        User.username: form.username,
        User.password: hash_password(form.password),
        User.role: form.role,
        User.is_active: form.is_active,
    })
    db.commit()
    return True
