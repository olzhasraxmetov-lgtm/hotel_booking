from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mapppers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper
