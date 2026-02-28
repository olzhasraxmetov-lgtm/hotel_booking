from src.schemas.facilities import FacilityCreate
from src.services.base import BaseService
from src.tasks.tasks import test_task

class FacilitiesService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityCreate):
        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()  # type: ignore
        return facility