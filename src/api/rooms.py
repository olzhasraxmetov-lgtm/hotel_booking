from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.exceptions.exceptions import (
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomsPatchRequest
from src.services.rooms import RoomsService

router = APIRouter(prefix="/{hotel_id}/rooms")


@router.get("/", tags=["Номера"])
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples=["2026-02-05"]),
    date_to: date = Query(examples=["2026-02-18"]),
):
    return await RoomsService(db).get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


@router.get("/{room_id}", tags=["Номера"])
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/", tags=["Номера"])
async def create_room(hotel_id: int, db: DBDep, payload: RoomAddRequest = Body(...)):
    try:
        room = await  RoomsService(db).create_room(hotel_id=hotel_id, payload=payload)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "ok", "data": room}


@router.delete("/{room_id}", tags=["Номера"])
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomsService(db).delete_room(hotel_id=hotel_id, room_id=room_id)
    return {"status": "ok:"}


@router.put("/{room_id}", tags=["Номера"])
async def update_room(hotel_id: int, room_id: int, db: DBDep, payload: RoomAddRequest = Body(...)):
    await RoomsService(db).update_room(
        hotel_id=hotel_id, room_id=room_id, payload=payload
    )

    return {"status": "ok:"}


@router.patch("/{room_id}", tags=["Номера"])
async def partially_update_room(hotel_id: int, room_id: int, db: DBDep, payload: RoomsPatchRequest):
    await RoomsService(db).partially_update_room(
        hotel_id=hotel_id, room_id=room_id, payload=payload
    )
    return {"status": "ok:"}
