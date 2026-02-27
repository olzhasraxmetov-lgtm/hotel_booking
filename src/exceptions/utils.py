from datetime import date
from fastapi import HTTPException


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail='Дата заезда не может быть раньше даты выезда')
