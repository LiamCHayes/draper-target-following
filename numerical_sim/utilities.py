import numpy as np


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
