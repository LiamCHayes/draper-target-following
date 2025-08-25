"""First order CBF implementation for a moving target - numerical simulation"""

import numpy as np
import matplotlib.pyplot as plt
from qpsolvers import solve_qp
from celluloid import Camera
from tqdm import tqdm
from utilities import angleToRotationMatrix, drawHalfCone


class Simulation:
    def __init__(self):
        # Time related data
        self.T = 50.000
        self.dt = 0.001
        self.t = 0.0
        self.time_stamps = []

        # Agent state
        self.position = np.array([0.0, 0.0, 0.0])
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.phi = 0.0
        self.theta = 0.0
        self.psi = 0.0
        self.R = angleToRotationMatrix(0.0, 0.0, 0.0)
        self.omega = np.array([0.0, 0.0, 0.0])

        # Agent camera paramters
        self.FOV = np.pi / 6.0
        self.camera_axis = np.array([1.0, 0.0, 0.0])

        # Feature(s) state
        self.features = []

        # Things to track
        self.positions = []  # History of position
        self.norm_ep = []  # Position error over time
        self.norm_ev = []  # Velocity error over time

        # Animation
        self.animation_fig = plt.figure(1)
        self.animation_axis = plt.axes(projection="3d")
        self.camera = Camera(self.animation_fig)

    def run(self):
        for frame in tqdm(range(len(np.arange(0.0, self.T, self.dt)))):
            # Update time step
            self.t += self.dt
            self.time_stamps.append(self.t)

            # Compute agent control input
            self.compute_u_star()  # PD function in numerical sim
            self.apply_cbf()  # CBF function in numerical sim

            # Update agent state
            self.position = self.position + self.velocity_control * self.dt
            self.positions.append(self.position)

            # Save frame for animation
            if frame % 33 == 0:
                self.add_frame()

        # Create a dataframe with all tracked things for analysis TODO

    def compute_u_star(self):
        """Computes the nominal trajectory before applying the CBF"""
        # PD controller constants
        K_p = 20.8  # Position error gain
        K_d = 13.3  # Velocity error gain

        # Calculate desired trajectory
        rx = 1.0
        omega_x = 0.3

        ry = 10.0
        omega_y = 0.2

        rz = 2.0
        omega_z = 0.2

        # Calculate desired position and velocity
        self.p_des = np.array(
            [
                rx * np.sin(omega_x * self.t),
                ry * np.sin(omega_y * self.t),
                rz * np.sin(omega_z * self.t),
            ]
        )

        self.v_des = np.array(
            [
                omega_x * rx * np.cos(omega_x * self.t),
                omega_y * ry * np.cos(omega_y * self.t),
                omega_z * rz * np.cos(omega_z * self.t),
            ]
        )

        # Calculate control input
        self.velocity_control = (
            self.v_des
            - K_p * (self.position - self.p_des)
            - K_d * (self.velocity - self.v_des)
        )
        self.norm_ep.append(self.position - self.p_des)
        self.norm_ev.append(self.velocity - self.v_des)

    def apply_cbf(self):
        """
        Solves the CBF QP and applies the result

        Uses the library qp_solvers, which needs:
        - P, the quadratic term matrix. A positive semi-definite matrix and symmetric matrix that defines the curvature of the quadratic objective. Typically the hessian matrix of second derivatives
        - q, the linear term vector. Corresponds to the linear weights applied to the variables
        - G and h, inequality constraints for the optimization problem
        - A and b, equality constraints for the optimization problem
        - lb and ub, lower and upper bounds for the optimization problem

        In the context of the CBF, how do we define each of these terms that go into qpsolvers.solve_qp?
        
        TODO
        - Write out the first order optimization problem in terms of P, q, G, h, A, b, lb, and ub.
        - Implement this in the code
        """
        # Calculate current direction of camera axis in world frame
        z = self.R @ self.camera_axis

        # Initialize QP variables

        # Initialize CBF constants

        # Loop through each feature to compute the CBF constraint for each feature

        # Impose additional constraints to improve robustness

        # Define the cost matrix for the QP and solve

        # Update the control input

        # Store relevant metrics to track

    def animation(self):
        """Make a video of the drone following the target"""
        print("Creating animation")
        animation = self.camera.animate()
        animation.save("plots/animation.mp4", writer="ffmpeg", fps=30)
        print("Done")

    def add_frame(self):
        self.animation_axis.plot(
            self.position[0], self.position[1], self.position[2], "ob"
        )
        self.animation_axis.plot(self.p_des[0], self.p_des[1], self.p_des[2], "og")
        for f in self.features:
            self.animation_axis.plot(f[0], f[1], f[2], "xr")

        drawHalfCone(
            self.animation_axis, self.position, self.FOV, R=self.R, plot_type="circle"
        )

        self.animation_axis.set_title("Agent FOV")
        self.animation_axis.set_xlabel("x (m)")
        self.animation_axis.set_ylabel("y (m)")
        self.animation_axis.set_zlabel("z (m)")
        self.animation_axis.set_xlim([-5.0, 10.0])
        self.animation_axis.set_ylim([-5.0, 5.0])
        self.animation_axis.set_zlim([-5.0, 5.0])

        self.camera.snap()

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
