from fastapi import Query, APIRouter, Body, Depends

from sqlalchemy import insert, select, or_

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])






@router.get("", summary="Получение информации об отелях")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Город и адрес"),
        title: str | None = Query(None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels

    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]






@router.post("", summary="Создание отеля")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "ул. Морячки, 3",
    }},
    "2": {"summary": "Дубай", "value": {
            "title": "Дубай возле фонтана",
            "location": "ул. Шэйха, 4",
    }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # Дебаг запросов, создаваемых SQLAlchemy
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

        return {"status": "OK"}



@router.put("/{hotel_id}", summary="Обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK", "hotel": hotel}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title is not None:
        hotel["title"] = hotel_data.title
    if hotel_data.name is not None:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}



@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
