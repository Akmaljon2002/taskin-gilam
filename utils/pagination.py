from math import ceil
from datetime import datetime
import pytz
from fastapi import HTTPException


def pagination(form, page, limit):
    if page and limit:
        return {"current_page": page, "limit": limit, "pages": ceil(form.count() / limit),
                "data": form.offset((page - 1) * limit).limit(limit).all()}
    return form.all()


def save_in_db(db, obj):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def the_one(db, model, id):
    the_one = db.query(model).filter(model.id == id).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"Bazada bunday {model} yo'q!")
    return the_one


def is_datetime_valid(input_datetime_str):
    try:
        input_datetime = datetime.strptime(input_datetime_str, '%Y-%m-%d %H:%M:%S')
        toshkent_timezone = pytz.timezone('Asia/Tashkent')
        current_time_toshkent = datetime.now(toshkent_timezone)
        input_datetime_toshkent = toshkent_timezone.localize(input_datetime)
        return input_datetime_toshkent >= current_time_toshkent
    except ValueError:
        return False


allowed_image_types = ["image/png", "image/jpg", "image/jpeg"]
allowed_video_types = ["video/mp4", "video/avi"]
allowed_audio_types = ["audio/mp3", "audio/wav"]  # Audio fayllar
allowed_voice_types = ["audio/ogg", "audio/mpeg"]  # Ovozli habar fayllari
allowed_document_types = ["application/pdf", "application/msword"]  # Hujjat fayllari
allowed_other_types = ["application/octet-stream"]  # Boshqa fayl formatlari


allowed_address_source = ["customers"]
allowed_phones_source = ["customers", "user", "market"]
