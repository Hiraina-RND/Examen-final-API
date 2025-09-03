from typing import List

from fastapi import FastAPI
from pydantic.v1 import BaseModel
from starlette.responses import PlainTextResponse, JSONResponse, HTMLResponse

app = FastAPI()


@app.get("/ping")
def ping():
    return PlainTextResponse("pong")

class Characteristics(BaseModel):
    max_speed: int
    max_fuel_capacity: int


class car_model(BaseModel):
    id: str
    brand: str
    model: str
    characteristics: Characteristics

car_list : List[car_model] = []


@app.post("/cars")
def create_cars_list(new_car_list: List[car_model]):
    if len(new_car_list) == 0:
        return JSONResponse(status_code=400, content={"message": "List cannot be empty"})
    car_list.extend(new_car_list)
    return JSONResponse(status_code=201, content={"New cars list": car_list})

@app.get("/cars")
def get_cars():
    return JSONResponse(status_code=200, content={"cars": car_list})


@app.get("/cars/{id}")
def read_car(id: str):
    for car in car_list:
        if car.id == id:
            return JSONResponse(status_code=200, content={car})
    return JSONResponse(status_code=404, content={"message": "Car not found"})

