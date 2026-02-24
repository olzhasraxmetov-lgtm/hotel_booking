import json

import pytest
from httpx import ASGITransport, AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_poll
from src.main import app
from src.models import *
from src.schemas.hotels import HotelCreate
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

data_hotels_path = BASE_DIR / 'mock_hotels.json'
data_rooms_path = BASE_DIR / 'mock_rooms.json'

@pytest.fixture(scope='session', autouse=True)
def check_test_mode():
    assert settings.MODE == 'TEST'



@pytest.fixture(scope='session',autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session',autouse=True)
async def setup_test_data(setup_database):
    with (
        open(data_hotels_path, encoding='utf-8') as file_hotels,
        open(data_rooms_path, encoding='utf-8') as file_rooms
    ):
        hotels_data = json.load(file_hotels)
        rooms_data = json.load(file_rooms)

    hotels_data_to_create = [HotelCreate(**hotel) for hotel in hotels_data]
    rooms_data_to_create = [RoomsAdd(**room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        await db.hotels.add_bulk(hotels_data_to_create)
        await db.rooms.add_bulk(rooms_data_to_create)

        await db.commit()

@pytest.fixture(scope='session',autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
         await ac.post('/auth/register', json={
            "email": "olzhas@gmail.com",
            "password": "12345",
        })
