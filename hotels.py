from fastapi import Query, Body, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hotels", tags=["Отели"])



hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id":2, "title": "Dubai", "name": "dubai"},
]



@router.get("", summary="Получение информации об отелях")
def get_hotels(
        id: int | None = Query(None,description="Айдишник"),
        title: str | None = Query(None,description="Название отеля"),
):

    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

class Hotel(BaseModel):
    title: str
    name: str


@router.post("", summary="Создание отеля")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] +1,
        "title": hotel_data.title,
        "name" : hotel_data.name,
    })
    return {"status": "OK"}



@router.put("/{hotel_id}", summary="Обновление данных об отеле")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK", "hotel": hotel}



@router.patch("/{hotel_id}", summary="Частичное обновление данных об отеле")
def partially_update_hotel(
        hotel_id: int,
        title : str | None = Body(None),
        name : str | None = Body(None),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if title is not None:
        hotel["title"] = title
    if name is not None:
        hotel["name"] = name
    return {"status": "OK"}



@router.delete("/{hotel_id}", summary="Удаление отеля")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
