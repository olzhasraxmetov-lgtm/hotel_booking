from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, \
    AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def create_booking(
    db: DBDep,
    payload: BookingAddRequest,
    user_id: UserIdDep,
):
    try:
        booking = await BookingService(db).add_booking(user_id, payload)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
