import pandas as pd
import pytest

from nbodyproblem.models.bodies import Point, Velocity, Acceleration, CelestialBody
from nbodyproblem.solver import main

def test_nbody_simulation():
    starting_point_earth = Point(1.496e11, 0)  # Earth on orbit around the sun
    starting_point_sun = Point(0, 0)  # Sun at origin

    velocity_earth = Velocity(0, 29780)  # Earth's orbital velocity around Sun ~29.78 km/s
    velocity_sun = Velocity(0, 0)  # Assuming the Sun is stationary in this frame

    mass_earth = 5.972e24  # Mass of Earth in kg
    mass_sun = 1.989e30  # Mass of Sun in kg

    zero_acc = Acceleration(0, 0)

    body_earth = CelestialBody("Earth", mass_earth, 6371, starting_point_earth, velocity_earth, zero_acc)
    body_sun = CelestialBody("Sun", mass_sun, 696340, starting_point_sun, velocity_sun, zero_acc)

    end_time = 3.156e7  # Simulate for one year (in seconds)
    time_step = 3600 * 24 * 7  # Time step of one week (in seconds)

    result = main([body_earth, body_sun], end_time, time_step)

    # Check if the result is a DataFrame
    assert isinstance(result, pd.DataFrame)

    # Check if the DataFrame has the expected columns
    expected_columns = ["time", "body", "x", "y", "vx",     uvicorn api:app --reload"vy", "ax", "ay"]
    assert all(column in result.columns for column in expected_columns)

    # Check if the DataFrame contains data for both Earth and Sun
    assert "Earth" in result["body"].values
    assert "Sun" in result["body"].values

    # Check if the simulation ran for the expected duration
    assert result["time"].max() == pytest.approx(end_time, rel=1e-2)

    # Check if the positions and velocities are not all zeros
    assert not result[["x", "y", "vx", "vy"]].eq(0).all().all()

if __name__ == "__main__":
    pytest.main()