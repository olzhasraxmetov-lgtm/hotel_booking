from datetime import date

from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM
from sqlalchemy import insert, select, func

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_by_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_id_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.hotel_id.in_(rooms_ids_to_get))
        )
        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_id_to_get))

        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel) for hotel in result.scalars().all()]