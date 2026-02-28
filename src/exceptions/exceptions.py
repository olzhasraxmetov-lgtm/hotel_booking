from fastapi import HTTPException


class AppBaseException(Exception):
    detail = "Непредвиденная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(AppBaseException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(AppBaseException):
    detail = "Не осталось свободных номеров"


class ObjectAlreadyExistException(AppBaseException):
    detail = "Похожий объект уже существует"

class RoomNotFoundException(AppBaseException):
    detail = "Номер не найден"

class HotelNotFoundException(AppBaseException):
    detail = "Отель не найден"

class UserAlreadyExistException(AppBaseException):
    detail = 'Пользователь уже существует'

class UserEmailAlreadyExistHTTPException(AppBaseException):
    status_code = 409
    detail = 'Пользователь с таким email уже существует'

class AppBaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(AppBaseHTTPException):
    status_code = 404
    detail = "Отель не найден"

class EmailNotRegisteredException(AppBaseHTTPException):
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordException(AppBaseHTTPException):
    detail = "Пароль неверный"

class IncorrectTokenException(AppBaseHTTPException):
    detail = "Некорректный токен"


class RoomNotFoundHTTPException(AppBaseHTTPException):
    status_code = 404
    detail = "Номер не найден"

class IncorrectTokenHTTPException(AppBaseHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(AppBaseHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(AppBaseHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class AllRoomsAreBookedHTTPException(AppBaseHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"

class IncorrectPasswordHTTPException(AppBaseHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(AppBaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"