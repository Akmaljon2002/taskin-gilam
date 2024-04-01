from models.models import Orders, Filial


def check_limit_def(user, db):
    filial = db.query(Filial).filter(Filial.filial_id == user.filial_id).first()
    buyurtma_olish_state = True
    joriy_buyurtma_count = db.query(Orders).filter(
        Orders.order_filial_id == user.filial_id,
        Orders.order_status.notin_(['topshirildi', 'keltirish', 'kutish', 'bekor qilindi'])).count()
    if joriy_buyurtma_count >= filial.buyurtma_limit:
        buyurtma_olish_state = False
    buyurtma_qoldi_limit = filial.buyurtma_limit - joriy_buyurtma_count
    if buyurtma_qoldi_limit < 0:
        buyurtma_qoldi_limit = 0
    return {"buyurtma_olish_state": buyurtma_olish_state, "buyurtma_qoldi_limit": buyurtma_qoldi_limit}

