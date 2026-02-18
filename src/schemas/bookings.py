from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingBase(BaseModel):
    date_from: date
    date_to: date


class BookingAddRequest(BookingBase):
    room_id: int


class BookingAdd(BookingAddRequest):
    price: int
    user_id: int


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
