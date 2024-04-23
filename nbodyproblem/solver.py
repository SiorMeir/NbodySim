import numpy as np
from scipy.constants import gravitational_constant as G
from nbodyproblem.models.bodies import Acceleration, CelestialBody, Force, Point, Velocity

def calc_gravity(m1,m2,r):
    return (m1 * m2 * G)/(r ** 2)

def calc_forces(bodies : list[CelestialBody]) -> dict:
    forces_in_system = {}

    for i,body_i in enumerate(bodies):
        force_on_body_i = Force(0,0)  # Initialize force vector for body i

        for j,body_j in enumerate(bodies):
            if i != j:
                # Calculate distance between bodies i and j
                dist_vector = body_i.X.get_difference(body_j.X)

                # Calculate gravitational force
                force_magnitude = calc_gravity(body_j.mass,body_j.mass,dist_vector.size)
                force_direction = dist_vector.azimuth
                force = Force.from_polar(force_magnitude,force_direction)

                # Update force on body i
                force_on_body_i += force
        forces_in_system.update({body_i.name : force_on_body_i})
    return forces_in_system

def calc_eq_force(forces : list[Force]):
    cum_force = Force(0,0)

    for force in forces:
        cum_force = cum_force + force

    return cum_force

def update_body_state(body: CelestialBody,force : Force, timestep=0.1) -> CelestialBody:
    acceleration = Acceleration.from_polar(force.size / body.mass , force.azimuth)
    body.A += acceleration
    body.V += body.A * timestep
    body.X = body.X + body.V * timestep + body.A * 0.5 * timestep ** 2
    return body

def main(bodies : list[CelestialBody], endtime : int, timestep : int) -> None:
    timesteps = range(0,endtime,timestep)
    print(list(timesteps))
    print(forces)
    elapsed_time = 0.0
    while elapsed_time < endtime:
        forces = calc_forces(bodies)
        for body in bodies:
            update_body_state(body,forces.get(body.name),timestep)
        # for each body, assign forces & update state
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

if __name__ == "__main__":
    starting_point_a = Point(0,0)
    starting_point_b = Point(10,0)
    zero_velocity = Velocity(0,0)
    zero_acc = Acceleration(0,0)
    body_a = CelestialBody("A",10,10,starting_point_a,zero_velocity,zero_acc)
    body_b = CelestialBody("B",10,10,starting_point_b,zero_velocity,zero_acc)
    main([body_a,body_b],10,1)