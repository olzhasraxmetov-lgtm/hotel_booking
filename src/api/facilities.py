from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilityCreate

router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get('/')
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post('/')
async def create_facility(
        db: DBDep,
        data: FacilityCreate = Body(),
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": 201, "facility": facility}