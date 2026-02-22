from fastapi import APIRouter, Body
import json
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import FacilityCreate
from src.init import redis_connector
router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get('/')
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_connector.get('facilities')
    if not facilities_from_cache:
        print('going to db')
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_connector.set('facilities', facilities_json, expire=10)
        return facilities
    else:
        facilities_dict = json.loads(facilities_from_cache)
        return facilities_dict

@router.post('/')
async def create_facility(
        db: DBDep,
        data: FacilityCreate = Body(),
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": 201, "facility": facility}