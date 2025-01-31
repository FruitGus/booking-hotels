from fastapi import APIRouter, Body, HTTPException

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.models.rooms import RoomsOrm
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/rooms", summary="Получение информации о номерах")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)



@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение информации о номере")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)



@router.post("/{hotel_id}/rooms", summary="Создание номера")
async def create_room(hotel_id: int, room_data: RoomAddRequest = Body()):
#     openapi_examples={
#         "1": {"summary": "Номер Relax Spa Resort", "value":{
#             "title": "Одноместный Comfort plus",
#             "description": "Предназначен для размещения одного человека и комплектуется одной кроватью,"
#                            "санузлом и кондиционером",
#             "price": "5000",
#             "quantity": "3"
#         }}
# })
# ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()

        return {"status": "OK", "data": room}



@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, id=room_id)
        await session.commit()

        return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def partially_update_room(hotel_id: int, room_id:int, room_data: RoomPatchRequest):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"status": "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"status": "OK"}