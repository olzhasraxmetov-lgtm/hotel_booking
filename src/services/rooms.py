from datetime import date

from src.exceptions.exceptions import HotelNotFoundHTTPException, ObjectNotFoundException, HotelNotFoundException, \
    RoomNotFoundException
from src.exceptions.utils import check_date_to_after_date_from
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomsAdd, RoomsPatchRequest, RoomsPATCH, Room
from src.services.base import BaseService
from src.services.hotels import HotelsService


class RoomsService(BaseService):
    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )


    async def get_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(
            self,
            hotel_id: int,
            payload: RoomAddRequest
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in payload.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()

    async def update_room(
            self,
            hotel_id: int,
            room_id: int,
            payload: RoomAddRequest
    ):
        await HotelsService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        _room_data = RoomsAdd(hotel_id=hotel_id, **payload.model_dump())

        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id=room_id, facilities_ids=payload.facilities_ids
        )
        await self.db.commit()

    async def partially_update_room(
            self,
            hotel_id: int,
            room_id: int,
            payload: RoomsPatchRequest
    ):
        await HotelsService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        _room_data_dict = payload.model_dump(exclude_unset=True)
        _room_data = RoomsPATCH(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(data=_room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)

        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelsService(self.db).get_hotel_with_check(hotel_id=hotel_id)

        await self.get_room_with_check(room_id=room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException