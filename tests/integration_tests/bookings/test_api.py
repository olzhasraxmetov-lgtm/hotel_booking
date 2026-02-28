import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2026-02-01", "2026-02-10", 200),
        (1, "2026-02-02", "2026-02-11", 200),
        (1, "2026-02-03", "2026-02-12", 200),
        (1, "2026-02-04", "2026-02-13", 200),
        (1, "2026-02-05", "2026-02-14", 200),
        (1, "2026-02-06", "2026-02-15", 409),
        (1, "2026-02-17", "2026-02-23", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, authenticated_user):
    response = await authenticated_user.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, rooms_booked_number",
    [
        (1, "2026-02-01", "2026-02-07", 1),
        (1, "2026-02-02", "2026-02-09", 2),
        (1, "2026-02-03", "2026-02-10", 3),
    ],
)
async def test_add_and_get_my_booking(
    room_id,
    date_from,
    date_to,
    rooms_booked_number,
    authenticated_user,
    delete_all_bookings,
):
    response = await authenticated_user.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )

    assert response.status_code == 200
    response_my_bookings = await authenticated_user.get("/bookings/me")
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == rooms_booked_number
