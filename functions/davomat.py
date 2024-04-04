from datetime import datetime
import pytz
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from models.models import User, Davomat


def davomatlar_def(user, sana, db):
    davomat = db.query(Davomat).filter(
        User.filial_id == user.filial_id, User.status == 10).join(User).options(joinedload(Davomat.user.and_(
        User.filial_id == user.filial_id, User.status == 10)))
    today = datetime.now(pytz.timezone("Asia/Tashkent")).date()
    if not sana:
        sana = today
    davomat = davomat.filter(Davomat.sana == sana)

    return davomat.all()


def davomat_update_def(davomatlar_id, the_user, status, db):
    for davomat_id in davomatlar_id:
        davomat = db.query(Davomat).filter(Davomat.id == davomat_id, Davomat.filial_id == the_user.filial_id)
        if status == "keldi":
            davomat = davomat.filter(Davomat.keldi == 0).first()
            if davomat:
                davomat.keldi = 1
                davomat.ketdi = 0
                davomat.keldi_time = datetime.now(pytz.timezone('Asia/Tashkent'))
                davomat.ketdi_time = ""
                davomat.status = True
                davomat.type = 0
                maosh_q = 0
        elif status == "yarim":
            davomat = davomat.filter(Davomat.keldi == 1, Davomat.ketdi == 0).first()
            if davomat:
                davomat.keldi = 1
                davomat.ketdi = 1
                davomat.ketdi_time = datetime.now(pytz.timezone('Asia/Tashkent'))
                davomat.keldi_time = ""
                davomat.status = False
                davomat.type = 5
                maosh_q = 0.5
        elif status == "butun":
            davomat = davomat.filter(Davomat.keldi == 1, Davomat.ketdi == 0).first()
            if davomat:
                davomat.keldi = 1
                davomat.ketdi = 1
                davomat.ketdi_time = datetime.now(pytz.timezone('Asia/Tashkent'))
                davomat.keldi_time = ""
                davomat.status = False
                davomat.type = 10
                maosh_q = 1
        if davomat:
            user = davomat.user
            user.oylik += maosh_q*user.maosh

        db.commit()
    return True


