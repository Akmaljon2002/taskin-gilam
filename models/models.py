import pytz
from sqlalchemy import Column, Integer, String, Boolean, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password_hash = Column(String(255))
    auth_key = Column(String(32))
    status = Column(Integer)
    fullname = Column(String(255))
    filial_id = Column(Integer)
    maosh = Column(Integer)
    kpi = Column(Boolean)
    oylik = Column(Integer)
    role = Column(String(255))
    phone = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    balance = Column(Integer)
    moi_zvonki_user_name = Column(String(255))
    user_moi_zvonki_address = Column(String(255))
    user_moi_zvonki_api = Column(String(255))
    ozroq_kpi = Column(Boolean)
    plastik = Column(Integer)
    click = Column(Integer)
    phone2 = Column(String(15))
    zayavka_limit = Column(Integer)
    topshirish_limit = Column(Integer)
    skald_limit = Column(Integer)
    api_token = Column(String(255), default='')
    zakaz_status = Column(Integer)

    costumer = relationship('Costumers', back_populates='user')


class Costumers(Base):
    __tablename__ = "costumers"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, default=0)
    costumers_filial_id = Column(Integer, default=0)
    costumer_name = Column(String(255))
    costumer_phone_1 = Column(String(255))
    costumer_phone_2 = Column(String(255))
    costumer_phone_3 = Column(String(255), default='')
    costumer_addres = Column(String(255))
    customer_nationality = Column(String(255), default='')
    costumer_date = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    costumer_source = Column(String(255), default='')
    orienter = Column(String(255), default='')
    costumer_status = Column(String(255), default='')
    costumer_turi = Column(String(255), default='')
    saygak_id = Column(Integer, default=0)
    mintaqa_id = Column(Integer, default=0)
    manba = Column(String(100), default='')
    token = Column(String(100), default='')
    parol = Column(String(100), default='')
    user_id = Column(Integer, ForeignKey("user.id"))
    millat_id = Column(Integer, default=0)
    call_count = Column(Integer, default=0)
    calling = Column(Boolean, default=False)
    izoh = Column(String(255), default='')
    created_at = Column(TIMESTAMP, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(TIMESTAMP, default=0)

    user = relationship('User', back_populates='costumer')