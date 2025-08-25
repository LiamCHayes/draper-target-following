import numpy as np

# Constants
DIM = 3
I = np.eye(DIM)


# Rotations utilities
def xAxisRotation(theta):
    R = [
        [1.0, 0.0, 0.0],
        [0.0, np.cos(theta), -np.sin(theta)],
        [0.0, np.sin(theta), np.cos(theta)],
    ]
    R = np.array(R)
    return R


def yAxisRotation(theta):
    R = [
        [np.cos(theta), 0.0, np.sin(theta)],
        [0.0, 1.0, 0.0],
        [-np.sin(theta), 0.0, np.cos(theta)],
    ]
    R = np.array(R)
    return R


def zAxisRotation(theta):
    R = [
        [np.cos(theta), -np.sin(theta), 0.0],
        [np.sin(theta), np.cos(theta), 0.0],
        [0.0, 0.0, 1.0],
    ]
    R = np.array(R)
    return R


def angleToRotationMatrix(phi, theta, psi):
    # Roll (phi x), pitch (theta y), yaw (psi z)
    # Rotation formula: R_z * R_x * R_y
    # Meaning: first rotation about z, then around x, then around y (?)
    R = zAxisRotation(psi) @ xAxisRotation(phi) @ yAxisRotation(theta)
    return R


def rotationMatrixToAngle(R):
    yaw = np.arctan2(-R[0, 1], R[1, 1])
    roll = np.arcsin(R[2, 1])
    pitch = np.arctan2(-R[2, 0], R[2, 2])

    return roll, pitch, yaw


# Plotting functionalities
def drawHalfCone(
    axis, vertex, aperture, R=I.copy(), height=10.0, resolution=0.5, plot_type="circle"
):
    # Draw a half circular cone, default is with
    # axis parallel to the x axis of the plot
    # Parameters
    #            axis       : axis on which to draw
    #            vertex     : vertex of the cone
    #            aperture   : half the aperture of the cone
    #            R          : rotation matrix to rotate the cone
    #            height     : height of the cone
    #            resolution : distance between line/circles
    #            plot_type  : type of plot ("line", "circle")

    if plot_type != "line" and plot_type != "circle":
        print("Unknown plot type, using default type: circle")
        plot_type = "circle"

    if plot_type == "circle":
        # Plot the cone as a series of circles
        circles = []  # List to store circles
        depth = resolution  # Initialize depth
        while depth < height:  # Loop from vertex to total height
            radius = depth * np.tan(aperture)  # Radius of current circle
            current_circle = []  # List of points of the current circle
            for theta in np.arange(0, 2 * np.pi + 0.1, 0.1):  # Loop around the circle
                point = [
                    depth,
                    radius * np.cos(theta),
                    radius * np.sin(theta),
                ]  # Compute point on circle along x axis
                point = R @ np.array(
                    point
                )  # Rotate point to align with desired orientation
                point = point + vertex  # Add vertex coordinates
                current_circle.append(point)  # Add point to circle
            circles.append(current_circle)  # Add circle to list
            depth += resolution  # Update depth

        for circle in circles:
            axis.plot(
                [point[0] for point in circle],
                [point[1] for point in circle],
                [point[2] for point in circle],
                "b-",
                alpha=0.2,
            )

    if plot_type == "line":
        end_points = []
        radius = height * np.tan(aperture)
        for theta in np.arange(0, 2 * np.pi + 0.1, resolution):
            end_point = [height, radius * np.cos(theta), radius * np.sin(theta)]
            end_point = R @ np.array(end_point)
            end_point = end_point + vertex
            end_points.append(end_point)

        for end_point in end_points:
            axis.plot(
                [vertex[0], end_point[0]],
                [vertex[1], end_point[1]],
                "b-",
                zs=[vertex[2], end_point[2]],
                alpha=0.2,
            )
