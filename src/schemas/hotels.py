from pydantic import BaseModel


class HotelCreate(BaseModel):
    title: str
    location: str


class Hotel(HotelCreate):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
