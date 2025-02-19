from fastapi import Query, APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilitiesAddRequest

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение всех удобств")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Создание удобств")
async def create_facilities(db: DBDep, facility_data: FacilitiesAddRequest):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}