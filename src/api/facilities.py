from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityCreate
from src.services.facilities import FacilitiesService
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilitiesService(db).get_facilities()


@router.post("")
async def create_facility(
    db: DBDep,
    data: FacilityCreate = Body(),
):
    facility = await FacilitiesService(db).create_facility(data)
    return {"status": "OK", "data": facility}
