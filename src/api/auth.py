from fastapi import APIRouter, Body
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserCreate
from src.schemas.users import UserRequestCreate

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def login(
        data: UserRequestCreate = Body(openapi_examples={
            "1": {"summary": "Пользователь olzhas", "value": {
                "email": "olzhas@gmail.com",
                "password": "easypassword",
            }},
        })
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserCreate(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "success"}



@router.post("/login")
async def login():
    pass

@router.post("/logout")
async def login():
    pass