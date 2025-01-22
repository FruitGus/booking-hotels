from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
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
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


@router.get("/hotels/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id = hotel_id)



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
        hotel = await HotelsRepository(session).add(hotel_data)
        # Дебаг запросов, создаваемых SQLAlchemy
        # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.commit()

        return {"status": "OK", "data": hotel}



@router.put("/{hotel_id}", summary="Обновление данных об отеле")
async def update_hotel(hotel_id: None | int, hotel_data: Hotel):

    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
        await session.commit()

        return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}



@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
