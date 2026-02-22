from datetime import date

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mapppers import BookingDataMapper
from sqlalchemy import select

class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper


    async def get_bookings_today_with_check_in(self):
        query = (
            select(BookingsORM)
            .filter(BookingsORM.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]