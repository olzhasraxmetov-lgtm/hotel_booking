import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",[
    (1, "2026-02-01", "2026-02-10", 200),
    (1, "2026-02-02", "2026-02-11", 200),
    (1, "2026-02-03", "2026-02-12", 200),
    (1, "2026-02-04", "2026-02-13", 200),
    (1, "2026-02-05", "2026-02-14", 200),
    (1, "2026-02-06", "2026-02-15", 500),
    (1, "2026-02-17", "2026-02-23", 200)
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_user):
    response = await authenticated_user.post(
        '/bookings',
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert 'data' in res