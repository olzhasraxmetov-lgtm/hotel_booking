

async def test_get_hotels(ac):
    response = await ac.get('/hotels', params={
        "date_from": "2026-02-13",
        "date_to": "2026-02-19"
    })
    assert response.status_code == 200