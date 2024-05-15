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
                    body_j.mass, body_j.mass, dist_vector.size
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
    body.A += acceleration
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
    timesteps = range(0, endtime, timestep)
    dataseries = sim_dataseries.copy()
    print(list(timesteps))
    elapsed_time = 0.0
    while elapsed_time < endtime:
        forces = calc_forces(bodies)
        for body in bodies:
            temp_body = update_body_state(body, forces.get(body.name), timestep)
            dataseries = add_to_timeseries(dataseries, temp_body, elapsed_time)
        elapsed_time += timestep
    print(dataseries)
    return dataseries
    """
    Stages:
    1. get all bodies
    2. get all Forces between bodies == N-1 forces
    3. assign forces to bodies
    4. calc cumulative force for each body
    5. calc acceleration for each body
    6. calc velocity
    7. calc postion
    8. repeat for next time step
    """

def update_plot(frame):
    plt.cla()  # Clear the current axes
    data = df[df['time'] == frame]  # Filter data for the current time
    plt.scatter(data['x'], data['y'])  # Plot x and y coordinates for the body
    plt.xlim(0, max(df['x']))  # Set x-axis limits
    plt.ylim(0, max(df['y']))  # Set y-axis limits
    plt.title(f'Time: {frame}')  # Set title with current time


if __name__ == "__main__":
    starting_point_a = Point(0, 0)
    starting_point_b = Point(10, 0)
    zero_velocity = Velocity(0, 0)
    zero_acc = Acceleration(0, 0)
    body_a = CelestialBody("A", 10, 10, starting_point_a, zero_velocity, zero_acc)
    body_b = CelestialBody("B", 10, 10, starting_point_b, zero_velocity, zero_acc)
    df = main([body_a, body_b], 10, 1)

    fig = plt.figure()
    ani = animation.FuncAnimation(fig, update_plot, frames=df['time'].unique(), blit=False)
    plt.show()
