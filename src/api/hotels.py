from datetime import date

from fastapi import Query, APIRouter, Body


from src.schemas.hotels import HotelAdd, HotelPATCH

from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("", summary="Получение информации об отелях")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2025-01-01"),
        date_to: date = Query(example="2025-01-10"),

):
    per_page = pagination.per_page or 5
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
    )


    # if pagination.page and pagination.per_page:
    #     return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]


@router.get("/hotels/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id = hotel_id)



@router.post("", summary="Создание отеля")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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

    hotel = await db.hotels.add(hotel_data)
    # Дебаг запросов, создаваемых SQLAlchemy
    # print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
    await db.commit()

    return {"status": "OK", "data": hotel}



@router.put("/{hotel_id}", summary="Обновление данных об отеле")
async def update_hotel(hotel_id: None | int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
async def partially_update_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}



@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}
