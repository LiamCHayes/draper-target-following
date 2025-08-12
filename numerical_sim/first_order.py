"""First order CBF implementation for a moving target - numerical simulation"""

import numpy as np
from tqdm import tqdm
from utilities import angleToRotationMatrix


class Simulation:
    def __init__(self):
        # Time related data
        self.T = 100.000
        self.dt = 0.001
        self.t = 0.0
        self.time_stamps = []

        # Agent state
        self.position = np.array([0.0, 0.0, 0.0])
        self.veloctiy = np.array([0.0, 0.0, 0.0])
        self.phi = 0.0
        self.theta = 0.0
        self.psi = 0.0
        self.R = angleToRotationMatrix(0.0, 0.0, 0.0)
        self.omega = np.array([0.0, 0.0, 0.0])

        # Agent camera paramters
        self.FOV = np.pi / 6.0
        self.camera_axis = np.array([1.0, 0.0, 0.0])

        # Agent control input
        self.velocity_control = None
        self.angular_velocity_control = None

        # Feature(s) state
        self.features = []

    def run(self):
        for _ in tqdm(np.arange(0.0, self.T, self.dt)):
            # Update time step
            self.t += self.dt
            self.time_stamps.append(self.t)

            # Compute agent control input
            self.compute_u_star()
            self.apply_cbf()

            # Update agent state TODO

    def compute_u_star(self):
        """Computes the nominal trajectory before applying the CBF"""
        # TODO
        pass

    def apply_cbf(self):
        """Solves the CBF QP and applies the result"""
        # TODO
        pass

    def animation(self):
        """Make a video of the drone following the target"""
        # TODO
        pass

    def plot(self):
        """Plots important values over time for debugging"""
        # TODO
        pass


def main():
    simulation = Simulation()
    simulation.run()
    simulation.animation()
    simulation.plot()


if __name__ == "__main__":
    main()
