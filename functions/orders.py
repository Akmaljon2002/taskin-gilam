from sqlalchemy.orm import joinedload, defer, load_only
from models.models import Orders
from utils.pagination import pagination


def all_orders(search, page, limit, db):
    orders = db.query(Orders).options(
        load_only("order_id", "operator_id", "izoh", "izoh2", "order_price", "order_last_price", "order_driver",
                  "finish_driver", "order_date", "olibk_sana", "top_sana", "ch_sum", "ch_foiz", "own"),
        joinedload("cleans").options(load_only("clean_hajm", "gilam_eni", "gilam_boyi", "clean_narx", "narx", "user_id",
                                               "joy", "qad_user")))
    if search:
        search_formatted = "%{}%".format(search)
        orders = orders.filter(
            Orders.nomer.like(search_formatted) | Orders.saygak_id.like(search_formatted))
    return pagination(orders, page, limit)


def one_order(id, db):
    return db.query(Orders).filter(Orders.order_id == id).options(joinedload("operator").options(
        defer("password_hash"), defer("auth_key"), defer("username")), joinedload("filial"), joinedload("mintaqa")).first()

