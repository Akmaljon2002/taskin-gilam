from schemas.washing import CleanStatus


def yuvish_to_qadoqlash(status):
    rest_status = None
    if status == CleanStatus.QAYTA_YUVISH.value:
        rest_status = CleanStatus.QAYTA_QURIDI.value

    elif status == CleanStatus.OLCHOV.value or status == CleanStatus.YUVILMOQDA.value:
        rest_status = CleanStatus.QURIDI.value;

    else:
        rest_status = status

    return rest_status
