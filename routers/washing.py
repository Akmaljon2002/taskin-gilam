import inspect
from datetime import datetime
import pytz
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db import get_db
from functions.buyurtma import select_buyurtma_first, update_buyurtma_value, insert_buyurtma
from functions.orders import update_order, order_get, order_first
from functions.washing import clean_filter_fililal_and_status_count, clean_select_with_xizmat, \
    clean_with_status, insert_clean, clean_first, update_clean
from functions.xizmatlar import select_xizmat_firsrt
from routers.auth import current_active_user
from schemas.orders import OrderYuvishGetResponse, OrderYuvishResponse
from schemas.users import UserCurrent
from schemas.washing import Yuvilmaganlar_yuvilganlar_qadoqlanganlarResponse, CleanStatus, YuvishAndQaytaYuvish
from schemas.xizmatlar import XizmatCleanCountResponse, XizmatYuvishPost, XizmatYuvishPut
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification
from utils.status_path import yuvish_to_qadoqlash

router_washing = APIRouter()


@router_washing.get('/unwashed_washed_packed', summary="Chaqirish", status_code=200)
async def unwashed_washed_packed_get(db: Session = Depends(get_db),
                                     current_user: UserCurrent = Depends(current_active_user)) -> \
        Yuvilmaganlar_yuvilganlar_qadoqlanganlarResponse:
    """
        ## Yuvilganlar, yuvilmaganlar va qanoqlanganlarni sonini chaqirib olish
    """
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    washing = {
        "yuvilmagan": clean_filter_fililal_and_status_count(db, current_user.filial_id, [
            CleanStatus.YUVILMOQDA.value,
            CleanStatus.OLCHOV.value,
            CleanStatus.QAYTA_YUVISH.value,
        ]),
        "yuvilgan": clean_filter_fililal_and_status_count(db, current_user.filial_id, [
            CleanStatus.QURIDI.value,
            CleanStatus.QAYTA_QURIDI.value,
        ]),
        "qadoqlangan": clean_filter_fililal_and_status_count(db, current_user.filial_id, [
            CleanStatus.QADOQLANDI.value,
            CleanStatus.QAYTA_QADOQLANDI.value,
        ])
    }
    return washing


@router_washing.get('/WashAndRewash', status_code=200)
async def yuvish_get(turi: YuvishAndQaytaYuvish, page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                     current_user: UserCurrent = Depends(current_active_user)) -> PaginationResponseModel[
    OrderYuvishGetResponse]:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Yuvilmagan va qayta yuvilgan buyurtmlarni chaqirib olamiz
    """

    data = None
    if turi == YuvishAndQaytaYuvish.yuvish.value:
        data = order_get(page, limit, db, current_user.filial_id, [
            CleanStatus.YUVILMOQDA.value,
            CleanStatus.OLCHOV.value
        ])
    else:
        data = order_get(page, limit, db, current_user.filial_id, [
            CleanStatus.QAYTA_YUVISH.value,
        ])

    return data


@router_washing.get('/costumer', summary="Buyurtma va mijoz", status_code=200)
async def washing_costumer(order_id: int, db: Session = Depends(get_db),
                           current_user: UserCurrent = Depends(current_active_user)) -> OrderYuvishResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## "order_id"si yuborilgan buyurtma va mijoz ma'lumotlari keladi
    * **xizmat_id** - yuqoridagi **/yuvish** va **/qayta_yuvish** "api"larida kelgan "order_id" yuboriladi
    """

    return order_first(db, order_id, current_user.filial_id);


@router_washing.get('/product', summary="Buyurtma maxsulotlarini chaqirish",
                    status_code=status.HTTP_200_OK)
async def yuvish_clean_mahsulot_get(order_id: int, db: Session = Depends(get_db),
                                    current_user: UserCurrent = Depends(current_active_user)) -> \
        XizmatCleanCountResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## "order_id"si yuborilgan buyurtmani barcha mahsulotlari (barcha bo'limlardagi) va yuvish keral bo'lganlari keladi
    * **xizmat_id** - yuqoridagi **/yuvish** va **/qayta_yuvish** "api"larida kelgan "order_id" yuboriladi
    """

    cleans = clean_select_with_xizmat(db, order_id, current_user.filial_id)
    yuvilmagan = clean_with_status(db, order_id, [CleanStatus.OLCHOV.value, CleanStatus.QAYTA_YUVISH.value,
                                                  CleanStatus.YUVILMOQDA.value])
    data = {
        'mahsulot_all': cleans,
        'mahsulot': yuvilmagan,
        'yuvilmagan': len(yuvilmagan),
    }

    return data


@router_washing.post('/product_add', summary="Buyurtma uchun yangi mahsulot qo'shish",
                     status_code=status.HTTP_200_OK)
async def washing_product_add(order_id: int, payload: XizmatYuvishPost, db: Session = Depends(get_db),
                              current_user: UserCurrent = Depends(current_active_user)) -> \
        XizmatCleanCountResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buyurtmaga yangi mahsulot qo'shish
    """

    # Bunday ximat mavjudligini tekshirib olamiz
    xizmat = select_xizmat_firsrt(db, payload.xizmat_id, current_user.filial_id)

    # Tegishli buyurtmani chaqirib unga qo'shilgan mahsulot sonini yozip qo'yamiz
    buyurtma = select_buyurtma_first(db, order_id=order_id, x_id=payload.xizmat_id)
    if buyurtma:
        buyurtma = update_buyurtma_value(db, buyurtma.id, buyurtma.value)
    else:
        buyurtma = insert_buyurtma(db, {
            'filial_id': current_user.filial_id,
            'x_id': payload.xizmat_id,
            'order_id': order_id
        })

    # Cleani qo'shib olamiz
    clean_hajm = 0
    if xizmat.olchov == 'dona':
        clean_hajm = 1

    clean = insert_clean(db, {
        'order_id': order_id,
        'clean_filial_id': current_user.filial_id,
        'costumer_id': payload.costumer_id,
        'clean_product': payload.xizmat_id,
        'clean_status': CleanStatus.YUVILMOQDA.value,
        'clean_hajm': clean_hajm,
    })
    if buyurtma and clean:
        # ---------
        # SMS SEND
        # ---------
        data = await yuvish_clean_mahsulot_get(order_id, db, current_user)
        return data


@router_washing.put('/product_update', summary="Buyurtma mahsulotini o'zgartirish",
                    status_code=status.HTTP_202_ACCEPTED)
async def washing_product_put(order_id: int, payload: XizmatYuvishPut, db: Session = Depends(get_db),
                              current_user: UserCurrent = Depends(current_active_user)) -> XizmatCleanCountResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buyurtma mahsulotni razmerlarini o'zgartirish
    """

    # O'zgartirish kerak bo'lgan mahsulotni chaqirib olamiz
    clean = clean_first(db, payload.clean_id)
    if not clean:
        raise HTTPException(status_code=400, detail="Clean not found!")

    # Eski narxini o'zgaruvchiga biriktirib olamiz chalg'imaslig uchun (clean_narx * clean_hajm)
    clean_eski_narx = clean.clean_narx
    # payloda orqali kelgan narx (buyurtmani yuvish narxi) va hajmini (hajm buyurtma hajmi) ko'paytirib
    # tannarxini hisoblab olamiz
    clean_yangi_narx = payload.narx * payload.hajm

    clean_update = update_clean(db, clean.id, {
        'clean_status': yuvish_to_qadoqlash(clean.clean_status),
        "clean_hajm": payload.hajm,
        "gilam_eni": payload.eni,
        "gilam_boyi": payload.boy,
        'narx': payload.narx,
        'clean_narx': clean_yangi_narx,
        'clean_filial_id': current_user.filial_id,
        'user_id': current_user.id,
        'clean_date': datetime.now(pytz.timezone('Asia/Tashkent'))
    })
    order = order_first(db, order_id, current_user.filial_id, joinload=False)

    # Yulmaganlar qolmaganini tekshiramiz
    yuvilmagan = clean_with_status(db, order_id, [CleanStatus.OLCHOV.value, CleanStatus.QAYTA_YUVISH.value,
                                                  CleanStatus.YUVILMOQDA.value])

    order_status = order.order_status
    # Barchasi yuvilgan bo'lsa Buyurtma statusini o'zgartiramiz
    if len(yuvilmagan) == 0:
        order_status = yuvish_to_qadoqlash(order_status)

    # orderga buyurtmani umumiy narxini yozilgani uchun uni ham hisoblab  yozip qo'yamiz
    order_update = update_order(db, order_id, {
        'order_price': (order.order_price + clean_yangi_narx - clean_eski_narx),
        'order_status': order_status
    })

    # Ikki update muvofaqiyatli bo'lsa yangilangan ma'lumotlarni qayatramiz
    if order_update and clean_update:
        data = await yuvish_clean_mahsulot_get(order_id, db, current_user)
        return data

