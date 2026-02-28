# ruff: noqa: E402
import json
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_poll
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels import HotelCreate
from src.schemas.rooms import RoomsAdd
from src.utils.db_manager import DBManager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

data_hotels_path = BASE_DIR / "mock_hotels.json"
data_rooms_path = BASE_DIR / "mock_rooms.json"


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_poll) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def setup_test_data(setup_database):
    with (
        open(data_hotels_path, encoding="utf-8") as file_hotels,
        open(data_rooms_path, encoding="utf-8") as file_rooms,
    ):
        hotels_data = json.load(file_hotels)
        rooms_data = json.load(file_rooms)

    hotels_data_to_create = [HotelCreate(**hotel) for hotel in hotels_data]
    rooms_data_to_create = [RoomsAdd(**room) for room in rooms_data]

    async with DBManager(session_factory=async_session_maker_null_poll) as db_:
        await db_.hotels.add_bulk(hotels_data_to_create)
        await db_.rooms.add_bulk(rooms_data_to_create)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "olzhas@gmail.com",
            "password": "12345",
        },
    )


@pytest.fixture(scope="session")
async def authenticated_user(register_user, ac):
    await ac.post(
        "/auth/login",
        json={
            "email": "olzhas@gmail.com",
            "password": "12345",
        },
    )
    assert ac.cookies["access_token"]
    yield ac
