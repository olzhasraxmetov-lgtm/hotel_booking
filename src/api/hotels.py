from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache
from src.api.dependencies import PaginationDep, DBDep
from src.api.rooms import router as hotels_router
from src.exceptions.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.exceptions.utils import check_date_to_after_date_from
from src.schemas.hotels import HotelCreate
from src.schemas.hotels import HotelPATCH

router = APIRouter(prefix="/hotels")


@router.get("", summary="Получить список отелей", tags=["Отели"])
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Hotel Location"),
    title: str | None = Query(None, description="Hotel Name"),
    date_from: date = Query(examples=["2026-02-05"]),
    date_to: date = Query(examples=["2026-02-18"]),
):
    per_page = pagination.per_page or 5
    check_date_to_after_date_from(date_from, date_to)

    return await db.hotels.get_by_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}", summary="Получить один отель", tags=["Отели"])
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}", summary="Удалить отель", tags=["Отели"])
async def delete_hotel(hotel_id: int, db: DBDep):
    try:
        await db.hotels.delete(id=hotel_id)
        await db.commit()
        return {"success": "ok:"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("", summary="Создать новый отель", tags=["Отели"])
async def create_hotel(
    db: DBDep,
    hotel_data: HotelCreate = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Отель Сочи Elite", "location": "Сочи, ул. Сочи, 1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Отель Дубай Delux", "location": "Дубай, Шех 1"},
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"success": "ok:", "data": hotel}


@router.put("/{hotel_id}", summary="Полностью обновить отель", tags=["Отели"])
async def update_hotel(hotel_id: int, db: DBDep, hotel_data: HotelCreate):
    try:
        await db.hotels.edit(data=hotel_data, id=hotel_id)
        await db.commit()

        return {"success": "ok:"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch("/{hotel_id}", summary="Частично обновить отель", tags=["Отели"])
async def update_hotel_partially(hotel_id: int, db: DBDep, hotel_data: HotelPATCH):
    try:
        await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await db.commit()

        return {"success": "ok:"}
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


router.include_router(hotels_router)
