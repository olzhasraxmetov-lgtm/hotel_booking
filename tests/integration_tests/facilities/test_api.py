from unittest.mock import patch

async def test_facilities_get(ac):
    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_facilities_create(ac):
    facility_title = "test facility 1"
    with patch("src.tasks.tasks.test_task.delay") as mocked_task:

        response = await ac.post("/facilities", json={"title": facility_title})
        res = response.json()
        assert response.status_code == 200
        assert isinstance(res, dict)
        assert res['data']['title'] == facility_title
        assert 'data' in res

        mocked_task.assert_called_once()