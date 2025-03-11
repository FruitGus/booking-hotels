from src.schemas.facilities import FacilityAdd


async def test_add_facilities(db):
    facility_data = FacilityAdd(title="Панорамное окно")
    new_facility_data = await db.facilities.add(facility_data)
    await db.commit()
    print(f"{new_facility_data=}")