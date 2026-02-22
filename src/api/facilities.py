from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityCreate
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get('/')
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post('/')
async def create_facility(
        db: DBDep,
        data: FacilityCreate = Body(),
):
    facility = await db.facilities.add(data)
    await db.commit()
    test_task.delay()
    return {"status": 201, "facility": facility}