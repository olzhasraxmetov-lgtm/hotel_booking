from fastapi import  Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep
router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]



@router.get("/", summary='Получить список отелей')
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Hotel ID"),
        title: str | None = Query(None, description="Hotel Name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_

@router.delete("/{hotel_id}", summary='Удалить отель')
async def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"success": "ok:"}



@router.post("", summary='Создать новый отель')
async def create_hotel(
        hotel_data: Hotel = Body(openapi_examples={
            "1": {"summary": 'Сочи', "value": {
            "title": "Отель Сочи",
            "name": "sochi_u_morya"
        }},
        "2": {"summary": 'Дубай', "value": {
            "title": "Отель Дубай",
            "name": "dubai"
        }}
})
):
    global hotels
    data = {
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    }
    hotels.append(data)
    return {"success": "ok:"}

@router.put("/{hotel_id}", summary='Полностью обновить отель')
async def update_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
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