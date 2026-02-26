import pytest

@pytest.mark.parametrize("email, password, status_code", [
    ("rakhmetov@gmail.com", "12345", 200),
    ("someoneelse@gmail.com", "else1231", 200),
    ("rakhmetov@gmail.com", "123123123", 401),
    ("neew_user@gmail.com", "else1231", 200),
    ("abcde", "else1231", 422),
])
async def test_auth_flow(email: str, password: str,status_code,ac):
    response_register = await ac.post('/auth/register', json={
        "email": email,
        "password": password,
    })
    assert response_register.status_code == status_code
    if status_code != 200:
        return

    response_login = await ac.post('/auth/login', json={
        "email": email,
        "password": password,
    })
    assert response_login.status_code == status_code
    assert ac.cookies.get('access_token')
    assert 'access_token' in response_login.json()

    get_me_response = await ac.get('/auth/me')
    data_my_profile = get_me_response.json()
    assert isinstance(data_my_profile, dict)
    assert get_me_response.status_code == 200
    assert data_my_profile['email'] == email
    assert 'id' in data_my_profile
    assert 'password' not in data_my_profile
    assert 'hashed_password' not in data_my_profile

    logout_response = await ac.post('/auth/logout')
    logout_data = logout_response.json()
    assert logout_response.status_code == status_code
    assert logout_data['status'] == 'success'
    assert not ac.cookies.get('access_token')