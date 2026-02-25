async def test_add_booking(db, authenticated_user):
    room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_user.post(
        '/bookings',
        json={
            "room_id": room_id,
            "date_from": "2026-02-13",
            "date_to": "2026-02-19"
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert 'data' in res