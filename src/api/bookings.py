from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post('/')
async def create_booking(
        db: DBDep,
        payload: BookingAddRequest,
        user_id: UserIdDep,
):
    room = await db.rooms.get_one_or_none(id=payload.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(price=room_price, user_id=user_id,  **payload.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "success", "data": booking}

