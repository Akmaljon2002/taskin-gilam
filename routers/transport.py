import inspect
from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db import get_db
from functions.branches import filial_first
from functions.buyurtma import select_all_buyurtma_with_status
from functions.orders import order_filter_fililal_and_status_and_order_driver_count, \
    order_tartiblanmagan_tartiblangan_haydovchilar_get, order_tartiblanmagan_tartiblangan_get, order_first, update_order
from functions.transport import one_driver, all_drivers
from functions.washing import clean_with_status_and_product, clean_with_status_and_product_sum
from routers.auth import current_active_user
from schemas.orders import OrderStatus, TartiblanganTartiblanmaganEnum, OrderFilterResponse, \
    OrderTayyorBuyurtmaResponse, OrderTartiblash, OrderTartiblashResponse, OrderKvitansiyaResponse, \
    TayyorKvitansiyaMahsulotResponse
from schemas.transport import BuyurtmaSkladTopshiriladiganResponse
from schemas.users import UserCurrent
from schemas.washing import CleanStatus
from utils.pagination import PaginationResponseModel
from utils.role_verification import role_verification

router_transport = APIRouter()


@router_transport.get('/', status_code=200)
async def get_drivers(driver_id: int = 0,
                      db: Session = Depends(get_db), current_user: UserCurrent = Depends(current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if driver_id:
        return one_driver(driver_id, current_user.filial_id, db)
    return all_drivers(current_user.filial_id, db)


@router_transport.get('/buyurtma_sklad_topshiriladigan',
                      summary="Buyurtma sklad va topshiriladiganlar sonini chiqarish",
                      status_code=status.HTTP_200_OK)
async def buyurtma_sklad_topshiriladigan(db: Session = Depends(get_db),
                                         current_user: UserCurrent = Depends(current_active_user)) -> \
        BuyurtmaSkladTopshiriladiganResponse:
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    """
    ## Buyurtma sklad va topshiriladiganlar sonini chiqarish
    """
    data = {
        "buyurtmalar": order_filter_fililal_and_status_and_order_driver_count(db, current_user.filial_id, [
            OrderStatus.KELTIRISH.value,
        ], current_user),
        "sklad": order_filter_fililal_and_status_and_order_driver_count(db, current_user.filial_id, [
            OrderStatus.OMBOR.value,
        ]),
        "topshiriladigan": order_filter_fililal_and_status_and_order_driver_count(db, current_user.filial_id, [
            OrderStatus.QADOQLANDI.value,
            OrderStatus.QAYTA_QADOQLANDI.value
        ])
    }

    return data


@router_transport.get('/tayyor/filter-hodimlar', summary="Buyurtmalarni transport hodimlari",
                      status_code=status.HTTP_200_OK)
async def tayyor_buyurtma_hodim_filter_get(turi: TartiblanganTartiblanmaganEnum, db: Session = Depends(get_db),
                                           current_user: UserCurrent = Depends(current_active_user)) -> \
        list[OrderFilterResponse]:
    """
    ## Tayyor buyurtmalarni hodimlar orqali filterlash uchun
    * id - Xa responsda bu ikki xil turi da **int** yoki **str**
    """

    # Path-da keladigan tartib va tartiblanmagan larni chaqirish uchun
    tartib_bool = False
    if TartiblanganTartiblanmaganEnum.tartiblangan.value == turi:
        tartib_bool = True

    # Barcha buyurtmasi bor hodimlar
    haydovchi = order_tartiblanmagan_tartiblangan_haydovchilar_get(db, current_user.filial_id, [
        OrderStatus.QAYTA_QADOQLANDI.value,
        OrderStatus.QADOQLANDI.value
    ], tartiblangan=tartib_bool)

    # Barcha buyurtmalar soni
    haydovchi.append({
        'id': 'all',
        'name': 'Barcha mijozlar',
        'count': order_tartiblanmagan_tartiblangan_get(db, 0, 0, current_user.filial_id, [
            OrderStatus.QAYTA_QADOQLANDI.value,
            OrderStatus.QADOQLANDI.value
        ], tartiblangan=tartib_bool, joinedload_table=False, count=True)
    })

    # Miojoz o'zi olib ketadigan buyurtmalar soni
    haydovchi.append({
        'id': 'own',
        'name': 'O`zi olib ketadi',
        'count': order_tartiblanmagan_tartiblangan_get(db, 0, 0, current_user.filial_id, [
            OrderStatus.QAYTA_QADOQLANDI.value,
            OrderStatus.QADOQLANDI.value
        ], tartiblangan=tartib_bool, joinedload_table=False, own=True, count=True)
    })

    # Joyida yuviladigan buyurtmalar soni
    haydovchi.append({
        'id': 'joyida',
        'name': 'Joyida yuvish',
        'count': order_tartiblanmagan_tartiblangan_get(db, 0, 0, current_user.filial_id, [
            OrderStatus.QAYTA_QADOQLANDI.value,
            OrderStatus.QADOQLANDI.value
        ], tartiblangan=tartib_bool, joinedload_table=False, joyida=True, count=True)
    })

    return haydovchi


@router_transport.get('/tayyor', summary="Tayyor buyurtmalarni chaqirish",
                      status_code=status.HTTP_200_OK)
async def tayyor_buyurtma_get(turi: TartiblanganTartiblanmaganEnum, filter: Union[int, str] = None, page: int = 1,
                              limit: int = 25, db: Session = Depends(get_db),
                              current_user: UserCurrent = Depends(current_active_user)) -> \
        PaginationResponseModel[OrderTayyorBuyurtmaResponse]:
    """
    ## Tayyor buyurtmalarni chaqirish
    * filter - filter qilinmasa bo'sh jo'natiladi agar filter qilinadigan bo'lsa /tayyor/filter-hodimlar/{turi} shu api dagi **id** filterga qo'yib yuboriladi
    * filter - filter **turi** **str** or **int**
    * filter - jo'natilmasa yoki all jo'natilsa barcha buyurtmalar keladi
    """

    # Path-da keladigan tartib va tartiblanmagan larni chaqirish uchun
    tartib_bool = False
    if TartiblanganTartiblanmaganEnum.tartiblangan == turi:
        tartib_bool = True

    order = order_tartiblanmagan_tartiblangan_get(db, page, limit, current_user.filial_id, [
        OrderStatus.QAYTA_QADOQLANDI.value,
        OrderStatus.QADOQLANDI.value
    ], tartiblangan=tartib_bool, filter=filter)

    return order


@router_transport.put('/tayyor/buyurtma-tartiblash', summary="Buyurtmani tariblash",
                      status_code=status.HTTP_200_OK)
async def tayyor_buyurtma_tartiblash(order_id: int, payload: OrderTartiblash, db: Session = Depends(get_db),
                                     current_user: UserCurrent = Depends(
                                         current_active_user)) -> OrderTartiblashResponse:
    """
    ## Buyurtmani tariblash
    """

    # # Bunday buyurtma bormi yoki yo'q tekshirib olamiz
    order_first(db, order_id, current_user.filial_id, joinload=False)

    order = update_order(db, order_id, {
        'tartib_raqam': payload.tartib_raqam,
        'izoh3': payload.izoh
    })
    if order:
        return HTTPException(status_code=200, detail="Saqlandi")
    else:
        return HTTPException(status_code=200, detail="Saqlanmadi xatolik yuz berdi")


@router_transport.get('/tayyor/kvitansiya', summary="Buyurtmani kv va olgan hodim",
                      status_code=status.HTTP_200_OK)
async def tayyor_kvitansiya(order_id: int, db: Session = Depends(get_db),
                            current_user: UserCurrent = Depends(current_active_user)) -> OrderKvitansiyaResponse:
    """
    ## Buyurtmaga tegishin kv va buyurtma olgan hodimni chaqirib olish
    """
    order = order_first(db, order_id, current_user.filial_id, operator_old=True)
    return order


@router_transport.get('/tayyor/kvitansiya/mahsulot', summary="Buyurtmani barcha mahsulotlari",
                      status_code=status.HTTP_200_OK)
async def tayyor_kvitansiya(order_id: int, db: Session = Depends(get_db),
                            current_user: UserCurrent = Depends(
                                current_active_user)) -> TayyorKvitansiyaMahsulotResponse:
    """
    ## Buyurtmani barcha mahsulotlari topshirish kerak bo'lganlari
    """
    filial = filial_first(db, current_user.filial_id)
    buyurtma = select_all_buyurtma_with_status(db, order_id)
    total_sum = 0
    total_absolute_cost = 0
    total_count = 0
    order = None
    for item in buyurtma:
        # Clean larni chaqirib olish
        cleans = clean_with_status_and_product(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ])

        # Clean larni jami summasini chaqirib olish
        cleans_sum = clean_with_status_and_product_sum(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ])
        total_absolute_cost += cleans_sum

        # Buyurtmani jami summasini olish
        total_sum += clean_with_status_and_product_sum(db, order_id=item.order_id, product=item.x_id, status=[
            CleanStatus.QADOQLANDI.value, CleanStatus.QAYTA_QADOQLANDI.value
        ], reclean_place=True)

        # Burtma sonini hisoblash
        total_count += len(cleans)

        # Order-ni list tashqarisida chiqaramiz chunki u bitta
        order = item.order

        delattr(item, 'order')
        setattr(item, 'cleans', cleans)
        setattr(item, 'cleans_total_summa', cleans_sum)

    # Buyurtma uchun skida ni hisoblash
    total_with_discount_cost = 0
    if not order:
        raise HTTPException(status_code=400, detail="Order not found!")
    if order.own == 0:
        total_with_discount_cost = float(total_sum)
        skidka = float(order.order_skidka_sum) + (total_with_discount_cost * float(order.order_skidka_foiz) / 100)
        if skidka <= total_with_discount_cost:
            total_with_discount_cost -= skidka
        else:
            total_with_discount_cost = 0
        discount_for_own = 100
    else:
        total_with_discount_cost = float(total_sum)
        if total_with_discount_cost > 0:
            discount_for_own = total_with_discount_cost / float(total_absolute_cost) * 100
        else:
            discount_for_own = 100

    # Yakuniy summa
    tolov_summa = total_with_discount_cost - order.avans
    return {
        'items': buyurtma,
        'total_count': total_count,
        'total_sum': total_sum,
        'tolov_summasi': tolov_summa,
        'skidka_foiz': order.order_skidka_foiz,
        'skidka_som': order.order_skidka_sum,
        'ozi_olib_ketsa': float(100 - discount_for_own) if discount_for_own < 100 else None,
        'braklik': order.brak if filial.order_brak == 1 else None,
        'dog': order.dog if filial.order_dog == 1 else None,
        'operator_izoh': order.izoh if order.izoh and order.izoh != 'to`ldirilmadi' else None,
        'kvitansiya_izoh': order.izoh2 if order.izoh2 and order.izoh2 != 'to`ldirilmadi' else None,
        'transport_izoh': order.izoh3 if order.izoh3 and order.izoh3 != 'to`ldirilmadi' else None,
    }
