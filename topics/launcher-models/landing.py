import math
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# wtf are these units? definitely not inches
fig = plt.figure(figsize=(12, 9))
arc = fig.add_subplot(projection='3d')
# 3d arc
arc.set_xlim3d(0, 10)
arc.set_ylim3d(-5, 5)
arc.set_zlim3d(0, 10)

X = 0
Y = 1
Z = 2
GRAVITY = np.array([0.0, 0.0, -9.81])

# Best to keep this at 0 0 0, but not necessary
CURRENT_POSITION = np.array([4.0, 1.0, 0.4])
ROBOT_VELOCITY = np.array([-2.0, -2.0, 0.0])
TARGET_LOCATION = np.array([2.0, 3.0, 0.0])

DESIRED_ANGLE = 52.0 / 180.0 * math.pi


def calculate_initial_vector(current_position: np.ndarray, current_velocity: np.ndarray, target_position: np.ndarray):
    # We have 3 points
    ground_vector = target_position - current_position
    ground_vector[Z] = 0
    d = np.linalg.norm(ground_vector)
    h = target_position[Z] - current_position[Z]
    x_hat = math.sqrt( (9.81/2*d*d) / (math.sin(DESIRED_ANGLE)/math.cos(DESIRED_ANGLE)*d - h) )
    ground_vector = ground_vector / np.linalg.norm(d) * x_hat

    y_hat = x_hat * math.sin(DESIRED_ANGLE)/math.cos(DESIRED_ANGLE)

    final = ground_vector
    final[Z] = y_hat
    final = final - current_velocity

    return final


def calculate_effective_vector(vectors: list[np.array]):
    # https://www.youtube.com/watch?v=BLuI118nhzc
    # Actual effective trajectory is the sum of all the motions
    # in our case, the linear movement of the robot and the release vector
    # but let's loop it just in case
    if vectors is None or len(vectors) == 0:
        return np.array([0, 0, 0])

    final_vector = vectors[0]
    for idx in range(1, len(vectors)):
        final_vector = final_vector + vectors[idx]
    return final_vector


def render(origin, initial_vector, other_vectors):
    plt.sca(arc)
    plt.cla()
    arc.set_xlim3d(0, 10)
    arc.set_ylim3d(-5, 5)
    arc.set_zlim3d(0, 10)

    current_vector = initial_vector
    current_location = origin

    x = [origin[X], ]
    y = [origin[Y], ]
    z = [origin[Z], ]
    timescale = 0.01
    # We're plotting with euler integration to keep it simple
    for timestep in range(700):
        current_location = current_location + current_vector * timescale
        # I made gravity negative, deal with it
        current_vector = current_vector + GRAVITY * timescale
        x.append(current_location[X])
        y.append(current_location[Y])
        z.append(current_location[Z])
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    arc.plot(x, y, z, label='Launch Path')

    # Additional vectors
    for (name, vector) in other_vectors.items():
        x = [origin[X], origin[X] + vector[X]]
        y = [origin[Y], origin[Y] + vector[Y]]
        z = [origin[Z], origin[Z] + vector[Z]]
        arc.plot(x, y, z, label=name)

    arc.legend()


def render_loop(vectors):
    calculated_vector = calculate_initial_vector(CURRENT_POSITION, ROBOT_VELOCITY, TARGET_LOCATION)
    vectors["aim vector"] = calculated_vector
    effective_vector = calculate_effective_vector([calculated_vector, ROBOT_VELOCITY])

    robov_x_loc = fig.add_axes((0.14, 0.02, 0.3, 0.03))
    robov_x_slider = Slider(
        ax=robov_x_loc,
        label='Robo Vel X',
        valmin=-4.0,
        valmax=4.0,
        valinit=float(ROBOT_VELOCITY[X]),
        valstep=0.01
    )
    robov_y_loc = fig.add_axes((0.66, 0.02, 0.3, 0.03))
    robov_y_slider = Slider(
        ax=robov_y_loc,
        label='Robo Vel Y',
        valmin=-4.0,
        valmax=4.0,
        valinit=float(ROBOT_VELOCITY[Y]),
        valstep=0.01
    )

    robop_x_loc = fig.add_axes((0.14, 0.12, 0.3, 0.03))
    robop_x_slider = Slider(
        ax=robop_x_loc,
        label='Robo PosX',
        valmin=0.0,
        valmax=8.0,
        valinit=float(CURRENT_POSITION[X]),
        valstep=0.01
    )
    robop_y_loc = fig.add_axes((0.66, 0.12, 0.3, 0.03))
    robop_y_slider = Slider(
        ax=robop_y_loc,
        label='Robo PosY',
        valmin=-5.0,
        valmax=5.0,
        valinit=float(CURRENT_POSITION[Y]),
        valstep=0.01
    )

    def update(val: float) -> Any:
        # Setup robot velocity
        robot_velocity = ROBOT_VELOCITY
        robot_velocity[X] = robov_x_slider.val
        robot_velocity[Y] = robov_y_slider.val
        vectors["robo vel"] = robot_velocity
        # Setup robot position
        robot_position = CURRENT_POSITION
        robot_position[X] = robop_x_slider.val
        robot_position[Y] = robop_y_slider.val
        vectors["target vec"] = (TARGET_LOCATION - robot_position)

        new_calculated_vector = calculate_initial_vector(robot_position, robot_velocity, TARGET_LOCATION)
        vectors["aim vector"] = new_calculated_vector
        new_effective_vector = calculate_effective_vector([new_calculated_vector, robot_velocity])
        render(robot_position, new_effective_vector, vectors)

    robov_x_slider.on_changed(update)
    robov_y_slider.on_changed(update)
    robop_x_slider.on_changed(update)
    robop_y_slider.on_changed(update)
    render(CURRENT_POSITION, effective_vector, vectors)
    plt.show()


def run():
    render_loop({
        "robo vel": ROBOT_VELOCITY,
        "target vec": (TARGET_LOCATION - CURRENT_POSITION)
    })


if __name__ == "__main__":
    run()
