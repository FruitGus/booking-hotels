import json
from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep

from src.init import redis_manager
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение всех удобств")
@cache(expire=10)
async def get_facilities(db: DBDep):
        print("ИДУ В БАЗУ ДАННЫХ")
        return await db.facilities.get_all()


@router.post("", summary="Создание удобств")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}