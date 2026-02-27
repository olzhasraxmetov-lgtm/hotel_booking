from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    db: DBDep,
    payload: BookingAddRequest,
    user_id: UserIdDep,
):
    try:
        room = await db.rooms.get_one(id=payload.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(price=room_price, user_id=user_id, **payload.model_dump())
    try:
        bookings = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409 ,detail=ex.detail)

    await db.commit()

    return {"status": "OK", "data": bookings}
