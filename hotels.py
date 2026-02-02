from fastapi import  Query, Body, APIRouter

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@router.get("/", summary='Получить список отелей')
async def get_hotels(
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
        title: str = Body(..., embed=True),
):
    global hotels
    data = {
        "id": hotels[-1]["id"] + 1,
        "title": title,
    }
    hotels.append(data)
    return {"success": "ok:"}

@router.put("/{hotel_id}", summary='Полностью обновить отель')
async def update_hotel(
        hotel_id: int,
        title: str = Body(...),
        name: str = Body(...),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"success": "ok:"}

@router.patch("/{hotel_id}", summary='Частично обновить отель')
async def update_hotel_partially(
        hotel_id: int,
        title: str | None = Body(default=None),
        name: str | None = Body(default=None),
):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if title:
                hotel["title"] = title
            elif name:
                hotel["name"] = name
    return {"success": "ok:"}