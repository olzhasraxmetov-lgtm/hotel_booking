from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import FacilityResponse, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilityResponse


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility