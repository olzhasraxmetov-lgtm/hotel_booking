from fastapi import  Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import Hotel
from src.repositories.hotels import HotelsRepository
router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

@router.get("/", summary='Получить список отелей')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Hotel Location"),
        title: str | None = Query(None, description="Hotel Name"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@router.delete("/{hotel_id}", summary='Удалить отель')
async def delete_hotel(
        hotel_id: int
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"success": "ok:"}



@router.post("", summary='Создать новый отель')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {"summary": 'Сочи', "value": {
            "title": "Отель Сочи Elite",
            "location": "Сочи, ул. Сочи, 1"
        }},
        "2": {"summary": 'Дубай', "value": {
            "title": "Отель Дубай Delux",
            "location": "Дубай, Шех 1"
        }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"success": "ok:", "data": hotel}

@router.put("/{hotel_id}", summary='Полностью обновить отель')
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()

    return {"success": "ok:"}

@router.patch("/{hotel_id}", summary='Частично обновить отель')
async def update_hotel_partially(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel['id'] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"success": "ok:"}