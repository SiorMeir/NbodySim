from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
from nbodyproblem.models.bodies import CelestialBody
from nbodyproblem.solver import main

app = FastAPI()

class CelestialBodyModel(BaseModel):
    name: str
    mass: float
    position: List[float]
    velocity: List[float]

@app.post("/simulate")
def simulate(bodies: List[CelestialBodyModel], endtime: int, timestep: int):
    body_list = [CelestialBody(body.name, body.mass, body.position, body.velocity) for body in bodies]
    result_df = main(body_list, endtime, timestep)
    return result_df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
