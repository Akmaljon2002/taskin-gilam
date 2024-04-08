import pytz
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Float, func, and_, Time
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True)
    password_hash = Column(String(255))
    auth_key = Column(String(32), default='')
    status = Column(Integer)
    fullname = Column(String(255))
    filial_id = Column(Integer)
    maosh = Column(Integer, default=0)
    kpi = Column(Boolean)
    oylik = Column(Integer)
    role = Column(String(255))
    phone = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    balance = Column(Integer, default=0)
    moi_zvonki_user_name = Column(String(255))
    user_moi_zvonki_address = Column(String(255))
    user_moi_zvonki_api = Column(String(255))
    ozroq_kpi = Column(Boolean)
    plastik = Column(Integer, default=0)
    click = Column(Integer, default=0)
    phone2 = Column(String(15))
    zayavka_limit = Column(Integer)
    topshirish_limit = Column(Integer, default=0)
    skald_limit = Column(Integer)
    api_token = Column(String(255), default='')
    zakaz_status = Column(Integer)

    costumer = relationship('Costumers', back_populates='user')
    order = relationship('Orders', back_populates='operator')
    clean = relationship('Clean', back_populates='user')

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.id, self.fullname, self.username)


class Costumers(Base):
    __tablename__ = "costumers"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, default=0)
    costumers_filial_id = Column(Integer, default=0)
    costumer_name = Column(String(255))
    costumer_phone_1 = Column(String(255), unique=True)
    costumer_phone_2 = Column(String(255), default="")
    costumer_phone_3 = Column(String(255), default='')
    costumer_addres = Column(String(255))
    customer_nationality = Column(String(255), default='')
    costumer_date = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    costumer_source = Column(String(255), default='')
    orienter = Column(String(255), default='')
    costumer_status = Column(String(255), default='kutish')
    costumer_turi = Column(String(255), default='sifat')
    saygak_id = Column(Integer, default=0)
    mintaqa_id = Column(Integer, default=0)
    manba = Column(String(100), default='sayt')
    token = Column(String(100), default=0)
    parol = Column(String(100), default=0)
    user_id = Column(Integer, ForeignKey("user.id"))
    millat_id = Column(Integer, ForeignKey("millat.id"), default=0)
    call_count = Column(Integer, default=0)
    calling = Column(Boolean, default=False)
    izoh = Column(String(255), default='')
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    user = relationship('User', back_populates='costumer')
    clean = relationship('Clean', back_populates='costumer')
    order = relationship('Orders', back_populates='costumer')
    millat = relationship('Millat', back_populates='costumer')

    def __repr__(self):
        return "<Costumer (id='{}', costumers_filial_id='{}', costumer_phone_1='{}')>".format(
            self.id, self.costumers_filial_id, self.costumer_phone_1)


class Filial(Base):
    __tablename__ = "filial"
    filial_id = Column(Integer, primary_key=True)
    filial_name = Column(String(255))
    filial_address = Column(String(255))
    filial_phone = Column(String(255))
    filial_director_id = Column(Integer)
    filial_work_date = Column(Date)
    filial_destination = Column(String(255))
    filial_status = Column(String(255))
    logo = Column(String(255))
    mini_logo = Column(String(255))
    order_dog = Column(Integer)
    order_brak = Column(Integer)
    mintaqa_id = Column(Integer)
    barcode = Column(Integer)
    balance = Column(Integer)
    transfer_driver = Column(Integer)
    adding_nation = Column(Integer)
    sizing = Column(Integer)
    changing_coast = Column(Integer)
    landing = Column(Boolean)
    sms_coast = Column(Integer)
    send_sms = Column(Boolean)
    country_id = Column(Integer)
    stilaj = Column(Boolean)
    costumer_input = Column(Integer)
    to_all_drivers = Column(Boolean)
    transfer_operator = Column(Boolean)
    transfer_admin_savdo = Column(Boolean)
    buyurtma_limit = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    order = relationship('Orders', back_populates='filial')

    def __repr__(self):
        return "<Kpi hisob (id='{}', xizmat_id='{}', summa='{}')>".format(
            self.id, self.xizmat_id, self.summa)


class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    nomer = Column(Integer, default=1)
    costumer_id = Column(Integer, ForeignKey("costumers.id"))
    order_filial_id = Column(Integer, ForeignKey("filial.filial_id"), default=0)
    order_date = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    olibk_sana = Column(DateTime)
    izoh = Column(String(255), default="to`ldirilmadi")
    order_price = Column(Integer, default=0)
    order_price_status = Column(String(111), default="_")
    order_last_price = Column(Integer, default=0)
    order_status = Column(String(255), default="keltirish")
    operator_id = Column(Integer, ForeignKey("user.id"))
    order_driver = Column(String(111), default="hamma")
    finish_driver = Column(Integer, default=0)
    geoplugin_longitude = Column(String(255), default="_")
    geoplugin_latitude = Column(String(255), default="_")
    order_skidka_foiz = Column(String(255), default=0)
    order_skidka_sum = Column(String(255), default=0)
    tartib_raqam = Column(Integer, default=0)
    topshir_sana = Column(Date, default="0000-00-00")
    dog = Column(String(255), default="yo'q")
    brak = Column(String(255), default="yo'q")
    top_sana = Column(DateTime, default="0000-00-00 00:00:00")
    saygak_id = Column(Integer, default=0)
    own = Column(Integer, default=0)
    mintaqa_id = Column(Integer, ForeignKey("mintaqa.id"), default=0)
    ch_foiz = Column(String(50), default=func.coalesce(order_skidka_foiz, '0'))
    ch_sum = Column(String(50), default=func.coalesce(order_skidka_sum, '0'))
    joyida = Column(Integer, default=0)
    called = Column(Integer, default=1)
    last_operator_id = Column(Integer, default=0)
    last_izoh = Column(String(111), default="null")
    talk_type = Column(String(255), default="null")
    talk_date = Column(DateTime, default="0000-00-00 00:00:00")
    last_operator_id2 = Column(Integer, default=0)
    last_izoh2 = Column(String(111), default="null")
    talk_type2 = Column(String(10), default="null")
    talk_date2 = Column(DateTime, default="0000-00-00 00:00:00")
    izoh2 = Column(String(255), default="null")
    izoh3 = Column(String(255), default="null")
    ombor_user = Column(Integer, default=0)
    haydovchi_satus = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))
    avans = Column(Integer, default=0)
    avans_type = Column(String(255))

    operator = relationship('User', back_populates='order')
    filial = relationship('Filial', back_populates='order')
    mintaqa = relationship('Mintaqa', back_populates='order')
    cleans = relationship('Clean', back_populates='order')
    costumer = relationship('Costumers', back_populates='order')
    mijoz_kirim = relationship('Mijoz_kirim', back_populates='order')

    driver = relationship('User', foreign_keys=[order_driver], primaryjoin=lambda: and_(User.id == Orders.order_driver))
    f_driver = relationship('User', foreign_keys=[finish_driver], primaryjoin=lambda: and_(
        User.id == Orders.finish_driver))
    last_operator = relationship('User', foreign_keys=[last_operator_id], primaryjoin=lambda: and_(
        User.id == Orders.last_operator_id))
    last_operator2 = relationship('User', foreign_keys=[last_operator_id2], primaryjoin=lambda: and_(
        User.id == Orders.last_operator_id2))

    @hybrid_property
    def cleans_count(self):
        return len(self.cleans)

    @hybrid_property
    def mijoz_kirim_summa(self):
        summa = 0
        for i in self.mijoz_kirim:
            if i.status == "olindi":
                summa += i.summa
        return summa

    def __repr__(self):
        return "<Clean (order_id='{}')>".format(
            self.order_id)


class Clean(Base):
    __tablename__ = "clean"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    clean_filial_id = Column(String(255))
    costumer_id = Column(Integer, ForeignKey("costumers.id"))
    sana = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    clean_date = Column(DateTime, default='0000-00-00 00:00:00')
    qad_date = Column(DateTime, default='0000-00-00 00:00:00')
    top_sana = Column(DateTime, default='0000-00-00 00:00:00')
    qayta_sana = Column(DateTime, default='0000-00-00 00:00:00')
    clean_product = Column(Integer, ForeignKey('xizmatlar.xizmat_id'))
    clean_status = Column(String(255))
    clean_hajm = Column(Float)
    gilam_eni = Column(Float, default=0)
    gilam_boyi = Column(Float, default=0)
    clean_narx = Column(Integer)
    narx = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    joy = Column(String(100), default='')
    qad_user = Column(Integer, default=0)
    barcode = Column(String(25))
    top_user = Column(Integer, default=0)
    reclean_place = Column(Integer, default=0)
    reclean_driver = Column(Integer, default=0)
    joyida_date = Column(DateTime, default='0000-00-00 00:00:00')
    joyida_user = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime, onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    user = relationship('User', back_populates='clean')
    xizmat = relationship('Xizmatlar', back_populates='cleans')
    order = relationship('Orders', back_populates='cleans')
    costumer = relationship('Costumers', back_populates='clean')
    driver = relationship('User', foreign_keys=[reclean_driver],
                          primaryjoin=lambda: and_(User.id == Clean.reclean_driver))

    def __repr__(self):
        return "<Clean (id='{}', order_id='{}', clean_status='{}')>".format(
            self.id, self.order_id, self.clean_status)


class Mintaqa(Base):
    __tablename__ = "mintaqa"
    id = Column(Integer, primary_key=True)
    name = Column(String(111))
    country_id = Column(Integer, ForeignKey("country.id"))
    created_at = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    country = relationship('Country', back_populates='mintaqa')
    order = relationship('Orders', back_populates='mintaqa')


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True)
    name = Column(String(111))
    tel_code = Column(Integer)
    tel_length = Column(Integer)
    language = Column(String(11))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    mintaqa = relationship('Mintaqa', back_populates='country')


class Mijoz_kirim(Base):
    __tablename__ = "mijoz_kirim"
    id = Column(Integer, primary_key=True)
    summa = Column(Integer, default=0)
    costumer_id = Column(Integer, ForeignKey("costumers.id"))
    status = Column(String(255))
    tolov_turi = Column(String(100))
    date = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    user_id = Column(Integer, ForeignKey("user.id"))
    kirim_izoh = Column(String(100), default='')
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    kassachi_id = Column(Integer, default=0)
    user_fullname = Column(String(100), default='')
    kassachi_fullname = Column(String(100), default='')
    costumer = Column(String(100), default='')
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    user = relationship('User')
    order = relationship('Orders', back_populates='mijoz_kirim')


class Nasiya(Base):
    __tablename__ = "nasiya"
    id = Column(Integer, primary_key=True)
    summa = Column(Integer, default=0)
    nasiyachi_id = Column(Integer, ForeignKey("costumers.id"))
    ber_date = Column(Date, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    status = Column(String(255))
    nasiya = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(Date)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    izoh = Column(String(111), default='')
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    order = relationship('Orders')
    nasiyachi = relationship('Costumers')


class Recall(Base):
    __tablename__ = "recall"
    recall_id = Column(Integer, primary_key=True)
    recall_filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    recall_costumer_phone = Column(String(255))
    recall_date = Column(Date)
    recall_time = Column(DateTime)
    recall_status = Column(String(255))
    izoh = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    operator_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    costumer = relationship('Costumers', foreign_keys=[recall_costumer_phone],
                            primaryjoin=lambda: and_(Costumers.costumer_phone_1 == Recall.recall_costumer_phone,
                                                     Costumers.costumers_filial_id == Recall.recall_filial_id))
    operator = relationship('User', foreign_keys=[operator_id],
                            primaryjoin=lambda: and_(User.id == Recall.operator_id))


class Xizmatlar(Base):
    __tablename__ = "xizmatlar"
    xizmat_id = Column(Integer, primary_key=True)
    xizmat_turi = Column(String(255))
    status = Column(String(115))
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    olchov = Column(String(255))
    narx = Column(Integer, default=0)
    min_narx = Column(Integer, default=0)
    saygak_narx = Column(Integer, default=0)
    discount_for_own = Column(Integer)
    operator_kpi_line = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    cleans = relationship('Clean', back_populates='xizmat')

    def __repr__(self):
        return "<Xizmat (xizmat_id='{}', xizmat_turi='{}', status='{}')>".format(
            self.xizmat_id, self.xizmat_turi, self.status)


class Kpi_hisob(Base):
    __tablename__ = "kpi_hisob"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    summa = Column(Integer, default=0)
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    date = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    order_id = Column(Integer, ForeignKey("orders.order_od"))
    clean_id = Column(Integer, ForeignKey("clean.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))


class Chegirma(Base):
    __tablename__ = "chegirma"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    xizmat_id = Column(Integer, ForeignKey("xizmatlar.xizmat_id"))
    summa = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))


class Millat(Base):
    __tablename__ = "millat"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    costumer = relationship('Costumers', back_populates='millat')


class Buyurtma(Base):
    __tablename__ = "buyurtma"
    id = Column(Integer, primary_key=True)
    x_id = Column(Integer, ForeignKey('xizmatlar.xizmat_id'))
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    value = Column(Float)
    status = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    xizmat = relationship('Xizmatlar')
    order = relationship('Orders')


class NasiyaBelgilash(Base):
    __tablename__ = 'nasiya_belgilash'
    id = Column(Integer, primary_key=True)
    foiz = Column(Float)
    summa = Column(Integer, default=0)
    filial_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))


class Sms_template(Base):
    __tablename__ = 'sms_template'
    id = Column(Integer, primary_key=True)
    filial_id = Column(Integer)
    keyword = Column(String(255))
    note = Column(String(255))
    text = Column(String(255))
    status = Column(Boolean)
    sms_driver = Column(Boolean)
    costumer_category = Column(String(255))
    delete_status = Column(Integer)


class Sms_setting(Base):
    __tablename__ = 'sms_setting'
    id = Column(Integer, primary_key=True)
    filial_id = Column(Integer)
    qadoqlanganda_status = Column(Boolean)
    yuvilganda_status = Column(Boolean)
    buyurtma_oln_status = Column(Boolean)
    transport_topshir = Column(Boolean)
    foydalanuvchi_qoshilganda = Column(Boolean)


class Sms_sended(Base):
    __tablename__ = 'sms_sended'
    id = Column(Integer, primary_key=True)
    filial_id = Column(Integer)
    costumer_id = Column(Integer)
    phone = Column(String(255))
    text = Column(String(255))
    date = Column(DateTime, default=datetime.now(pytz.timezone('Asia/Tashkent')))
    status = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))


class Fingerprint(Base):
    __tablename__ = 'fingerprint'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    token = Column(String(50))
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    date = Column(DateTime, default="0000-00-00 00:00:00")


class Davomat(Base):
    __tablename__ = 'davomat'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    sana = Column(Date)
    status = Column(Boolean)
    filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    keldi = Column(Boolean)
    ketdi = Column(Boolean)
    keldi_time = Column(Time)
    ketdi_time = Column(Time)
    maosh = Column(Integer)
    type = Column(String(50))
    sanavaqt = Column(DateTime)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))
    fingerprint_id = Column(Integer, ForeignKey("fingerprint.id"))

    fingerprint = relationship('Fingerprint')
    user = relationship('User')


class Kirim(Base):
    __tablename__ = 'kirim'
    kirim_id = Column(Integer, primary_key=True)
    kirim_user_id = Column(Integer)
    kirim_filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    kassachi_id = Column(Integer, ForeignKey("user.id"))
    kirim_summ = Column(Float)
    tolov_turi = Column(String(100))
    kirim_date = Column(DateTime)
    user_fullname = Column(String(100))
    kassachi_fullname = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))

    kassachi = relationship("User")
    hodim = relationship('User', foreign_keys=[kirim_user_id],
                         primaryjoin=lambda: and_(User.id == Kirim.kirim_user_id))


class Chiqim(Base):
    __tablename__ = 'chiqim'
    chiqim_id = Column(Integer, primary_key=True)
    chiqim_user_id = Column(Integer)
    chiqim_filial_id = Column(Integer, ForeignKey("filial.filial_id"))
    chiqim_summ = Column(Float)
    chiqim_firma = Column(Integer)
    chiqim_shaxsiy = Column(Integer)
    chiqim_izoh = Column(String(255))
    doimiy_izoh = Column(String(100))
    chiqim_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), default=datetime.now(pytz.timezone('Asia/Tashkent')))
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now(pytz.timezone('Asia/Tashkent')))
