from pydantic import BaseModel, ConfigDict

from src.schemas.facilities import FacilityResponse


class RoomAddRequest(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int
    facilities_ids: list[int] | None = []


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class Room(RoomsAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomWithRel(Room):
    facilities: list[FacilityResponse]


class RoomsPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomsPATCH(BaseModel):
    hotel_id: int | None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
