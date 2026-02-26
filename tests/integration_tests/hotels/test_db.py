from src.schemas.hotels import HotelCreate


async def test_add_hotel(db):
    hotel_data = HotelCreate(title="Test Hotel 1", location="Kenya")
    await db.hotels.add(hotel_data)
    await db.commit()
