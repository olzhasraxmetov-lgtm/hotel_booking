from fastapi import APIRouter, Body
from src.database import async_session_maker
from src.schemas.rooms import RoomsPATCH, Room, RoomsAdd, RoomAddRequest, RoomsPatchRequest
from src.repositories.rooms import RoomsRepository

router = APIRouter(prefix="/{hotel_id}/rooms")

@router.get("/", response_model=list[Room], tags=["Номера"])
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)

@router.get("/{room_id}", tags=["Номера"])
async def get_room(
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)

@router.post("/", tags=["Номера"])
async def create_room(hotel_id: int, payload: RoomAddRequest = Body(...)):
    _room_data = RoomsAdd(hotel_id=hotel_id,**payload.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "ok", "data": room}

@router.delete("/{room_id}", tags=["Номера"])
async def delete_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "ok:"}

@router.put("/{room_id}", tags=["Номера"])
async def update_room(
        hotel_id: int,
        room_id: int,
        payload: RoomAddRequest = Body(...)
):
    _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_room_data, id=room_id)
        await session.commit()
    return {"status": "ok:"}

@router.patch("/{room_id}", tags=["Номера"])
async def partially_update_room(
        hotel_id: int,
        room_id: int,
        payload: RoomsPatchRequest
):
    _room_data = RoomsPATCH(hotel_id=hotel_id, **payload.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()
    return {"status": "ok:"}