from datetime import date


from fastapi import APIRouter, Body, Query
from sqlalchemy import select, delete

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd, RoomFacility
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest



router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/rooms", summary="Получение информации о номерах")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2025-01-01"),
                    date_to: date = Query(example="2025-01-10"),
):

    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)



@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение информации о номере")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)



@router.post("/{hotel_id}/rooms", summary="Создание номера")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
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

    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}



@router.put("/{hotel_id}/rooms/{room_id}", summary="Обновление номера")
async def update_room(hotel_id: int,
                      room_id: int,
                      room_data: RoomAddRequest,
                      db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())

    await db.rooms.update(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()


    return {"status": "OK"}



@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def partially_update_room(hotel_id: int, room_id:int, room_data: RoomPatchRequest, db: DBDep):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, facilities_ids=_room_data_dict["facilities_ids"])

    await db.commit()

    return {"status": "OK"}



@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}