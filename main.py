import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]
@app.get("/hotels")
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

@app.delete("/hotels/{hotel_id}")
async def delete_hotel(
        hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {"success": "ok:"}

@app.post("/hotels")
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

@app.put("/hotels/{hotel_id}")
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

@app.patch("/hotels/{hotel_id}")
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


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)