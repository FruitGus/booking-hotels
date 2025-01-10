from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import uvicorn

app = FastAPI(docs_url=None)

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id":2, "title": "Dubai", "name": "dubai"},
]



@app.get("/hotels")
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

@app.post("/hotels")
def create_hotel(
        title: str = Body(),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] +1,
        "title": title
    })
    return {"status": "OK"}



@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title : str = Query(description = "Название отеля"),
        name : str  = Query(description = "Имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
                hotel["title"] = title
                hotel["name"] = name
                return {"status": "OK", "hotel": hotel}



@app.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title : str | None = Query(None, description = "Название отеля"),
        name : str | None = Query(None, description = "Имя отеля"),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title is not None:
                hotel["title"] = title
            if name is not None:
                hotel["name"] = name
            return {"status": "OK", "hotel": hotel}



@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

if __name__ == "__main__":
    uvicorn.run("main:app",  host="127.0.0.1", port=8001, reload=True)

