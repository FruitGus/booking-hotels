async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params = {
            "date_from": "2024-12-21",
            "date_to": "2025-01-15"
        }
    )
    print(f"{response.json()=}")

    assert response.status_code == 200