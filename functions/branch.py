from models.models import Filial


def filial_first(db, filial_id: int):
    return db.query(Filial).filter(Filial.filial_id == filial_id).first()