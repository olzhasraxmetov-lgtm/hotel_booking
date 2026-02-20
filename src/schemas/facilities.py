from pydantic import BaseModel, ConfigDict


class FacilityCreate(BaseModel):
    title: str

class FacilityPatch(BaseModel):
    title: str | None = None

class FacilityResponse(FacilityCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)