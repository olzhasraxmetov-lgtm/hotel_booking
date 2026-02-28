from datetime import date

from src.exceptions.exceptions import ObjectNotFoundException, HotelNotFoundException
from src.exceptions.utils import check_date_to_after_date_from
from src.schemas.hotels import HotelCreate, HotelPATCH, Hotel
from src.services.base import BaseService


class HotelsService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5

        return await self.db.hotels.get_by_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def create_hotel(self, hotel_data: HotelCreate):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_id: int, hotel_data: HotelCreate):
        await self.db.hotels.edit(data=hotel_data, id=hotel_id)
        await self.db.commit()

    async def update_hotel_partially(self,hotel_id: int, hotel_data: HotelPATCH):
        await self.db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException