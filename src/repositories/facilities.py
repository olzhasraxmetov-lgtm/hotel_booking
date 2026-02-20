from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import FacilityResponse


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = FacilityResponse
