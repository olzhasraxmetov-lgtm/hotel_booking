from pydantic import BaseModel, ConfigDict

class RoomAddRequest(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int

class Room(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)

class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None


class RoomsPATCH(BaseModel):
    hotel_id: int | None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None

