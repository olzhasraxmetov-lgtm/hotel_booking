from fastapi import  Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import HotelCreate
from src.repositories.hotels import HotelsRepository
from src.api.rooms import router as hotels_router
router = APIRouter(prefix="/hotels")

@router.get("/", summary='Получить список отелей', tags=["Отели"])
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

@router.get('/{hotel_id}', summary='Получить один отель',tags=["Отели"])
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}", summary='Удалить отель',tags=["Отели"])
async def delete_hotel(
        hotel_id: int
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"success": "ok:"}



@router.post("", summary='Создать новый отель',tags=["Отели"])
async def create_hotel(
        hotel_data: HotelCreate = Body(openapi_examples={
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

@router.put("/{hotel_id}", summary='Полностью обновить отель',tags=["Отели"])
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelCreate
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, id=hotel_id)
        await session.commit()

    return {"success": "ok:"}

@router.patch("/{hotel_id}", summary='Частично обновить отель',tags=["Отели"])
async def update_hotel_partially(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return {"success": "ok:"}

router.include_router(hotels_router)