import uvicorn
from fastapi import FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "name": "Sochi"},
    {"id": 2, "name": "Dubai"},
]
@app.get("/hotels")
async def get_hotels(
        id: int | None = Query(None, description="Hotel ID"),
        name: str | None = Query(None, description="Hotel Name"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if name and hotel["title"] != name:
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





if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)