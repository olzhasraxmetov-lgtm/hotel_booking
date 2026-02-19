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

    # async def get_all(self,location,title,limit,offset):
    #
    #     query = select(HotelsORM)
    #     if location:
    #         query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
    #     if title:
    #         query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #
    #     res = await self.session.execute(query)
    #     return [Hotel.model_validate(hotel) for hotel in res.scalars().all()]

    async def get_by_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        query = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.hotel_id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsORM.id.in_(query))