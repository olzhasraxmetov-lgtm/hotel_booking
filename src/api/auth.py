from fastapi import APIRouter, Body, HTTPException, Response, Request

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserCreate
from src.schemas.users import UserRequestCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def login(
        data: UserRequestCreate = Body(openapi_examples={
            "1": {"summary": "Пользователь olzhas", "value": {
                "email": "olzhas@gmail.com",
                "password": "easypassword",
            }},
        })
):
    hashed_password = AuthService.hash_password(data.password)
    new_user_data = UserCreate(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "success"}



@router.post("/login")
async def login_user(
        data: UserRequestCreate,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='Пользователь с таким email не существует')

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Пароль неверный')

        access_token = AuthService().create_access_token(data={"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.get("/auth_only")
async def logout(request: Request):
    access_token = request.cookies.get("access_token", None)
    data = AuthService().encode_auth_token(access_token)
    user_id = data["user_id"]
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user