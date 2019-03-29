#!/usr/bin/python

'''
Created on Oct 9, 2014

@author: Stefjord Todolli
'''

import copy
import numpy as np
from numpy import linalg
from scipy.optimize import leastsq

DELTA = 0.000000000001
GLOBAL_X = np.array([1.0, 0.0, 0.0])
GLOBAL_Y = np.array([0.0, 1.0, 0.0])
GLOBAL_Z = np.array([0.0, 0.0, 1.0])

def are_equal(f1, f2):
    return np.abs(f1 - f2) < DELTA



def rotate_structure_around_axis(pdb_structure, angle_radians, rotation_axis):
    rotated_pdb = copy.deepcopy(pdb_structure)
    axis_vector = np.array(rotation_axis[1])
    unit_vector = axis_vector / linalg.norm(axis_vector)
    R = get_rotationmatrix_around_vector(angle_radians, unit_vector)
    T = np.array(rotation_axis[0])
    for chain in rotated_pdb.all_chains:
        for residue in chain.residues:
            for atom in residue.atoms:
                translated_coordinate_list = np.array(atom.get_coords()) - T
                rotated_coordinates = np.dot(R, translated_coordinate_list) + T
                atom.set_coords(rotated_coordinates.tolist())
    return rotated_pdb


def rotate_nucleosome_around_superhelical_axis(pdb_structure, bp_frames, angle_radians, suphelical_axis=None):
    if suphelical_axis is None:
        suphelical_axis = find_superhelical_axis(bp_frames)
    return rotate_structure_around_axis(pdb_structure, angle_radians, suphelical_axis)


def get_rotationmatrix_around_vector(angle_radians, unit_vector):
    a = angle_radians
    u = unit_vector
    if not are_equal(linalg.norm(unit_vector), 1.0):
        u = unit_vector / linalg.norm(unit_vector)
    R = np.array([
                  [np.cos(a) + (1-np.cos(a))*np.power(u[0],2), u[0]*u[1]*(1-np.cos(a)) - u[2]*np.sin(a), 
                   u[0]*u[2]*(1-np.cos(a)) + u[1]*np.sin(a)
                   ], 
                  [u[0]*u[1]*(1-np.cos(a)) + u[2]*np.sin(a), np.cos(a) + (1-np.cos(a))*np.power(u[1],2), 
                   u[1]*u[2]*(1-np.cos(a)) - u[0]*np.sin(a)
                   ], 
                  [u[0]*u[2]*(1-np.cos(a)) - u[1]*np.sin(a), u[1]*u[2]*(1-np.cos(a)) + u[0]*np.sin(a), 
                   np.cos(a) + (1-np.cos(a))*np.power(u[2],2)
                   ]
                  ])
    return R


def find_superhelical_axis(bp_frames):
    bp_origins = [frame[1] for frame in bp_frames]
    bp_normals = [frame[2][2] for frame in bp_frames]
    starting_vector = __starting_axis_vector(bp_origins)
    starting_origin = np.array([0.0, 0.0, 0.0])
    axis_vector = leastsq(__angle_residuals, x0=starting_vector, args=bp_normals)[0]
    axis_vector = axis_vector / linalg.norm(axis_vector)
    axis_origin = leastsq(__radius_residuals, x0=starting_origin, args=[axis_vector, bp_origins])[0]
    return [axis_origin.tolist(), axis_vector.tolist()]


def get_linear_combination_of_vectors(vectors, coefficients):
    assert len(vectors) == len(coefficients)
    #assert are_equal(sum(coefficients), 1.0)
    new_vector = [0.0] * len(vectors[0])
    for _i in range(len(vectors)):
        new_vector = [new_vector[v] + coefficients[_i]*vectors[_i][v] for v in range(len(new_vector))]
    new_vector = new_vector / np.linalg.norm(new_vector)
    return new_vector.tolist()


def move_frame_along_vector(bp_frame, vector, distance):
    new_frame = copy.deepcopy(bp_frame)
    s = np.sqrt(np.power(distance,2)/sum(map(np.power, vector, [2, 2, 2])))
    new_frame[1] = [new_frame[1][_i] + s*vector[_i] for _i in range(len(new_frame[1]))]
    return new_frame


def __starting_axis_vector(bp_origins):
    bp_normal1 = bp_origins[10]
    bp_normal2 = bp_origins[80]
    axis_vector = np.array(bp_normal2) - np.array(bp_normal1)
    return axis_vector / linalg.norm(axis_vector)
    
def __angle_residuals(axis_vector, bp_normals):
    errs = []
    for normal in bp_normals:
        errs.append(np.dot(axis_vector, normal)/linalg.norm(axis_vector))
    return errs

def __radius_residuals(axis_origin, axis_vector_and_bp_origins):
    errs = []
    axis_vector = np.array(axis_vector_and_bp_origins[0])
    bp_origins = axis_vector_and_bp_origins[1]
    for origin in bp_origins:
        errs.append(__distance_from_point_to_line(axis_origin, axis_vector, origin))
    return errs

def __distance_from_point_to_line(axis_origin, axis_vector, point):
    x0 = np.array(point)
    x1 = np.array(axis_origin)
    x2 = np.array(axis_origin) + np.array(axis_vector)
    x1x2 = axis_vector
    crossp = np.cross(x0-x1, x0-x2)
    return linalg.norm(crossp)/linalg.norm(x1x2) 


