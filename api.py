from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from nbodyproblem.models.bodies import CelestialBody
from nbodyproblem.solver import main

app = FastAPI()

class CelestialBodyModel(BaseModel):
    name: str
    mass: float
    position: List[float]
    velocity: List[float]

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/simulate")
def simulate(bodies: List[CelestialBodyModel], endtime: int, timestep: int):
    body_list = [CelestialBody(body.name, body.mass, body.position, body.velocity) for body in bodies]
    result_df = main(body_list, endtime, timestep)
    return result_df.to_dict(orient='records')