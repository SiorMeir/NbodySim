import numpy as np
import pandas as pd
from scipy.constants import gravitational_constant as G
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from nbodyproblem.models.bodies import (
    Acceleration,
    CelestialBody,
    Force,
    Point,
    Velocity,
)
from nbodyproblem.models.timeseries import sim_dataseries, columns


def calc_gravity(m1, m2, r):
    return (m1 * m2 * G) / (r**2)


def calc_forces(bodies: list[CelestialBody]) -> dict:
    forces_in_system = {}

    for i, body_i in enumerate(bodies):
        force_on_body_i = Force(0, 0)  # Initialize force vector for body i

        for j, body_j in enumerate(bodies):
            if i != j:
                # Calculate distance between bodies i and j
                dist_vector = body_i.X.get_difference(body_j.X)

                # Calculate gravitational force
                force_magnitude = calc_gravity(
                    body_i.mass, body_j.mass, dist_vector.size
                )
                force_direction = dist_vector.azimuth
                force = Force.from_polar(force_magnitude, force_direction)

                # Update force on body i
                force_on_body_i += force
        forces_in_system.update({body_i.name: force_on_body_i})
    return forces_in_system


def calc_eq_force(forces: list[Force]):
    cum_force = Force(0, 0)

    for force in forces:
        cum_force = cum_force + force

    return cum_force


def update_body_state(body: CelestialBody, force: Force, timestep=0.1) -> CelestialBody:
    acceleration = Acceleration.from_polar(force.size / body.mass, force.azimuth)
    body.A = acceleration
    body.V += body.A * timestep
    body.X = body.X + body.V * timestep + body.A * 0.5 * timestep**2
    return body


def add_to_timeseries(
    timeseries: pd.DataFrame, body: CelestialBody, time: float
) -> pd.DataFrame:
    new_row = pd.DataFrame(
        data=[[
            time,
            body.name,
            body.X.x,
            body.X.y,
            body.V.x,
            body.V.y,
            body.A.x,
            body.A.y,
        ]],
        columns=columns,
    )
    timeseries = pd.concat(objs=[timeseries,new_row],ignore_index=True)
    return timeseries


def main(bodies: list[CelestialBody], endtime: int, timestep: int) -> pd.DataFrame:
    dataseries = sim_dataseries.copy()
    elapsed_time = 0.0
    while elapsed_time < endtime:
        forces = calc_forces(bodies)
        for body in bodies:
            temp_body = update_body_state(body, forces.get(body.name), timestep)
            dataseries = add_to_timeseries(dataseries, temp_body, elapsed_time)
        elapsed_time += timestep
    return dataseries

if __name__ == "__main__":
    starting_point_earth = Point(1.496e11,0)  # Earth on orbit around the sun
    starting_point_sun = Point(0, 0)  # Sun at origin

    velocity_earth = Velocity(0, 29780)  # Earth's orbital velocity around Sun ~29.78 km/s
    velocity_sun = Velocity(0, 0)  # Assuming the Sun is stationary in this frame

    mass_earth = 5.972e24  # Mass of Earth in kg
    mass_moon = 7.342e22  # Mass of Moon in kg
    mass_sun = 1.989e30  # Mass of Sun in kg

    zero_acc = Acceleration(0, 0)

    body_earth = CelestialBody("Earth", mass_earth, 6371, starting_point_earth, velocity_earth, zero_acc)
    body_sun = CelestialBody("Sun", mass_sun, 696340, starting_point_sun, velocity_sun, zero_acc)

    end_time = 3.156e+7  # Simulate for one year (in seconds)
    time_step = 3600 * 24 * 7 # Time step of one hour (in seconds)

    result = main([body_earth, body_sun], end_time, time_step)
    result.to_csv("result.csv", index=False)

    # Get unique bodies
    bodies = result['body'].unique()
    # Initialize the figure and axis
    fig, ax = plt.subplots()

    # Initialize data storage
    lines = {}
    for body in bodies:
        line, = ax.plot([], [], 'o', label=body)
        lines[body] = line

    ax.set_xlim(min(result['x']), max(result['x']))
    ax.set_ylim(min(result['y']), max(result['y']))
    ax.legend()

    # Initialization function
    def init():
        for line in lines.values():
            line.set_data([], [])
        return lines.values()

    # Update function
    def update(i):
        time_point = result['time'].unique()[i]
        for body in bodies:
            body_data = result[(result['body'] == body) & (result['time'] == time_point)]
            lines[body].set_data(body_data['x'], body_data['y'])
        return lines.values()

    # Create the animation
    frames = result['time'].unique()
    ani = animation.FuncAnimation(fig, update, frames=len(frames), init_func=init, blit=True)

    plt.show()