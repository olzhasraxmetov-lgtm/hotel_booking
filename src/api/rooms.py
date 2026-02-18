from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomsPATCH, Room, RoomsAdd, RoomAddRequest, RoomsPatchRequest

router = APIRouter(prefix="/{hotel_id}/rooms")

@router.get("/", response_model=list[Room], tags=["Номера"])
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)

@router.get("/{room_id}", tags=["Номера"])
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/", tags=["Номера"])
async def create_room(hotel_id: int, db: DBDep, payload: RoomAddRequest = Body(...)):
    _room_data = RoomsAdd(hotel_id=hotel_id,**payload.model_dump())
    room = await db.rooms.add(_room_data)
    await db.rooms
    return {"status": "ok", "data": room}

@router.delete("/{room_id}", tags=["Номера"])
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.rooms.commit()
    return {"status": "ok:"}

@router.put("/{room_id}", tags=["Номера"])
async def update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        payload: RoomAddRequest = Body(...)
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())
    await db.rooms.edit(data=_room_data, id=room_id)
    await db.rooms.commit()
    return {"status": "ok:"}

@router.patch("/{room_id}", tags=["Номера"])
async def partially_update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        payload: RoomsPatchRequest
):
    _room_data = RoomsPATCH(hotel_id=hotel_id, **payload.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
    await db.rooms.commit()
    return {"status": "ok:"}