from fastapi import FastAPI
from typing import List
from nbodyproblem.models.bodies import CelestialBody
from nbodyproblem.solver import main

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/simulate")
def simulate(bodies: List[CelestialBody], endtime: int, timestep: int):
    body_list = [
        CelestialBody(body.name, body.mass, body.position, body.velocity)
        for body in bodies
    ]
    result_df = main(body_list, endtime, timestep)
    return result_df.to_dict(orient="records")
