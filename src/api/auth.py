from fastapi import APIRouter, Body, HTTPException, Response, Depends

from src.api.dependencies import UserIdDep, DBDep
from src.database import async_session_maker
from src.exceptions.exceptions import ObjectAlreadyExistException
from src.schemas.users import UserCreate
from src.schemas.users import UserRequestCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def login(
    db: DBDep,
    data: UserRequestCreate = Body(
        openapi_examples={
            "1": {
                "summary": "Пользователь olzhas",
                "value": {
                    "email": "olzhas@gmail.com",
                    "password": "easypassword",
                },
            },
        }
    ),
):

    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserCreate(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
        await db.commit()
    except ObjectAlreadyExistException:
        raise HTTPException(status_code=409, detail='Пользователь с таким email уже существует')
    return {"status": "success"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestCreate, response: Response):
    async with async_session_maker():
        user = await db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не существует")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")

        access_token = AuthService().create_access_token(data={"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep = Depends):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}
