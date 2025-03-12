async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-12-21",
            "date_to": "2025-01-15",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert res["status"] == "OK"
    assert "data" in res