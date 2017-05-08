"""
    Stefjord Todolli
    May 08, 2017
"""

import numpy as np


ZERO = 0.000000000000001
ZERO2 = ZERO*ZERO
GLOBAL_O = np.array([0.0, 0.0, 0.0])
GLOBAL_X = np.array([1.0, 0.0, 0.0])
GLOBAL_Y = np.array([0.0, 1.0, 0.0])
GLOBAL_Z = np.array([0.0, 0.0, 1.0])
GLOBAL_FRAME = [GLOBAL_O, [GLOBAL_X, GLOBAL_Y, GLOBAL_Z]]
Cos = np.cos()
Sin = np.sin()


def frame_axes_matrix(frame):
    return np.array(frame[1]).T


def frame_origin_vector(frame):
    return np.array(frame[0])


def euler_angles_from_frames(frame1, frame2):
    dmat = np.dot(frame_axes_matrix(frame1).T, frame_axes_matrix(frame2))
    kappa = np.arccos(dmat[2, 2])
    if kappa * kappa < ZERO2:
        [zeta, kappa, eta] = [np.arctan2(dmat[1, 0], dmat[0, 0]), 0., 0.]
    else:
        zeta = np.arctan2(dmat[1, 2], dmat[0, 2])
        eta = np.arctan2(dmat[2, 1], -dmat[2, 0])
    if zeta + eta > np.pi:
        zeta -= 2 * np.pi / 2
    elif zeta + eta < -np.pi:
        zeta += 2 * np.pi
    return np.array([zeta, kappa, eta])


def euler_angles_from_angular_parameters(theta1, theta2, theta3):
    [t1, t2, t3] = np.radians([theta1, theta2, theta3])
    if t1 * t1 < ZERO2 and t2 * t2 < ZERO2:
        [zeta, kappa, eta] = [t3, 0., 0.]
    else:
        kappa = np.sqrt(t1 * t1 + t2 * t2)
        zeta = t3 / 2 - np.arctan2(t1, t2)
        eta = t3 / 2 + np.arctan2(t1, t2)
    return np.array([zeta, kappa, eta])


def rotation_matrix_D(theta1, theta2, theta3):
    [zeta, kappa, eta] = euler_angles_from_angular_parameters(theta1, theta2, theta3)
    return np.array([
        [Cos(zeta) * Cos(eta) * Cos(kappa) - Sin(zeta) * Sin(eta),
         -Cos(eta) * Sin(zeta) - Cos(zeta) * Cos(kappa) * Sin(eta),
         Cos(zeta) * Sin(kappa)],
        [Cos(eta) * Cos(kappa) * Sin(zeta) + Cos(zeta) * Sin(eta),
         Cos(zeta) * Cos(eta) - Cos(kappa) * Sin(zeta) * Sin(eta),
         Sin(zeta) * Sin(kappa)],
        [-Cos(eta) * Sin(kappa),
         Sin(eta) * Sin(kappa),
         Cos(kappa)]
    ])


def rotation_matrix_mid_step(theta1, theta2, theta3):
    [zeta, kappa, eta] = euler_angles_from_angular_parameters(theta1, theta2, theta3)
    return np.array([
        [Cos(zeta) * Cos((eta - zeta) / 2) * Cos(kappa / 2) - Sin(zeta) * Sin((eta - zeta) / 2),
         -Cos((eta - zeta) / 2) * Sin(zeta) - Cos(zeta) * Cos(kappa / 2) * Sin((eta - zeta) / 2),
         Cos(zeta) * Sin(kappa / 2)],
        [Cos((eta - zeta) / 2) * Cos(kappa / 2) * Sin(zeta) + Cos(zeta) * Sin((eta - zeta) / 2),
         Cos(zeta) * Cos((eta - zeta) / 2) - Cos(kappa / 2) * Sin(zeta) * Sin((eta - zeta) / 2),
         Sin(zeta) * Sin(kappa / 2)],
        [-Cos((eta - zeta) / 2) * Sin(kappa / 2),
         Sin((eta - zeta) / 2) * Sin(kappa / 2),
         Cos(kappa / 2)]
    ])


def rigid_body_parameters_step(frame1, frame2):
    [zeta, kappa, eta] = euler_angles_from_frames(frame1, frame2)
    theta1 = np.degrees(kappa * Sin((eta - zeta) / 2))
    theta2 = np.degrees(kappa * Cos((eta - zeta) / 2))
    theta3 = np.degrees(eta + zeta)
    midframe = np.dot(frame_axes_matrix(frame1), rotation_matrix_mid_step(theta1, theta2, theta3))
    [rho1, rho2, rho3] = np.dot(midframe.T, frame_origin_vector(frame2) - frame_origin_vector(frame1))
    return [theta1, theta2, theta3, rho1, rho2, rho3]


def rigid_body_parameters_steps_list(frames):
    rgb_parameters = []
    for _i in range(len(frames) - 1):
        rgb_parameters.append(rigid_body_parameters_step(frames[_i], frames[_i + 1]))
    return rgb_parameters


def RebuildFrame(rgb_parameters, frame0=GLOBAL_FRAME):
    rotmat = rotation_matrix_D(*rgb_parameters[:3].flatten())
    axes = np.dot(frame_axes_matrix(frame0), rotmat).T
    rotmat = rotation_matrix_mid_step(*rgb_parameters[:3].flatten())
    origin = np.dot(np.dot(frame_axes_matrix(frame0), rotmat),
                    rgb_parameters[3:].flatten()) + frame_origin_vector(frame0)
    return [origin, axes]


def RebuildFrames(rgb_parameters_list, frame0=GLOBAL_FRAME):
    frames = [frame0] * (len(rgb_parameters_list) + 1)
    for _i in range(len(rgb_parameters_list)):
        frames[_i + 1] = RebuildFrame(rgb_parameters_list[_i], frames[_i])
    return frames


def FramesTransformationMatrices(frame1, frame2):
    rotmat = np.dot(np.linalg.inv(np.array(frame1[1])), np.array(frame2[1]))
    tvect = frame_origin_vector(frame2) - frame_origin_vector(frame1)
    return (tvect, rotmat)
