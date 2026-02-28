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


class AppBaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(AppBaseHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(AppBaseHTTPException):
    status_code = 404
    detail = "Номер не найден"
