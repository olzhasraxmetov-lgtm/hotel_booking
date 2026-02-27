from datetime import date

from fastapi import APIRouter, Body, Query, HTTPException

from src.api.dependencies import DBDep
from src.exceptions.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException, RoomNotFoundHTTPException
from src.exceptions.utils import check_date_to_after_date_from
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomsPATCH, RoomsAdd, RoomAddRequest, RoomsPatchRequest

router = APIRouter(prefix="/{hotel_id}/rooms")


@router.get("/", tags=["Номера"])
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2026-02-05"]),
    date_to: date = Query(examples=["2026-02-18"]),
):
    check_date_to_after_date_from(date_from, date_to)
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{room_id}", tags=["Номера"])
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    room =  await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    if not room:
        raise RoomNotFoundHTTPException


@router.post("/", tags=["Номера"])
async def create_room(hotel_id: int, db: DBDep, payload: RoomAddRequest = Body(...)):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in payload.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "ok", "data": room}


@router.delete("/{room_id}", tags=["Номера"])
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException

    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok:"}


@router.put("/{room_id}", tags=["Номера"])
async def update_room(hotel_id: int, room_id: int, db: DBDep, payload: RoomAddRequest = Body(...)):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())

    await db.rooms.edit(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=payload.facilities_ids
    )
    await db.commit()

    return {"status": "ok:"}


@router.patch("/{room_id}", tags=["Номера"])
async def partially_update_room(hotel_id: int, room_id: int, db: DBDep, payload: RoomsPatchRequest):
    try:
        await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException
    try:
        await db.rooms.get_one(id=room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException

    _room_data_dict = payload.model_dump(exclude_unset=True)
    _room_data = RoomsPATCH(hotel_id=hotel_id, **_room_data_dict)
    await db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)

    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
        )
    await db.commit()
    return {"status": "ok:"}
