from models.models import Millat


def millatlar_get(user, db):
    millatlar = db.query(Millat).filter(Millat.filial_id == user.filial_id).all()
    return millatlar
