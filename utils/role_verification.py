from fastapi import HTTPException


def role_verification(user, function):

    allowed_functions_for_driver = ['get_orders_driver']

    if user.role == "admin":
        return True
    elif function in allowed_functions_for_driver:
        return True

    raise HTTPException(status_code=400, detail='Sizga ruhsat berilmagan!')

