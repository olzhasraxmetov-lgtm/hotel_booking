from src.database import async_session_maker_null_poll
from src.schemas.hotels import HotelCreate
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = HotelCreate(title='Test Hotel 1', location='Kenya')
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()