from fastapi import APIRouter, Body, Response, Depends

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions.exceptions import UserAlreadyExistException, \
    UserEmailAlreadyExistHTTPException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException
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
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistException:
        raise UserEmailAlreadyExistHTTPException

    return {"status": "success"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestCreate, response: Response):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException

    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(db: DBDep, user_id: UserIdDep = Depends):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}
