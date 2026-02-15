from pydantic import BaseModel, ConfigDict

class HotelCreate(BaseModel):
    title: str
    location: str

class Hotel(HotelCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None