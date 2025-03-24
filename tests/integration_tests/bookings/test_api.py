import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-12-21", "2024-12-29", 200),
    (1, "2024-12-21", "2024-12-23", 200),
    (1, "2024-12-21", "2024-12-27", 200),
    (1, "2024-12-21", "2024-12-22", 200),
    (1, "2024-12-21", "2025-12-25", 200),
    (1, "2024-12-21", "2025-01-15", 500),
])


async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res