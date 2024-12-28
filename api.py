from fastapi import FastAPI
from typing import List

from pydantic import BaseModel
from nbodyproblem.models.bodies import CelestialBody, Point, Velocity, Acceleration
from nbodyproblem.solver import main

app = FastAPI()


class SimulationRequest(BaseModel):
    bodies: List[CelestialBody]
    endtime: int
    timestep: int

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/simulate")
def simulate(request: SimulationRequest):
    result_df = main(request.bodies, request.endtime, request.timestep)
    return result_df.to_dict(orient="records")