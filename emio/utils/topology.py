import os.path

import Sofa
import numpy as np
from math import sin, cos, pi
from splib3.numerics import Quat, Vec3, vsub

from xml.dom import minidom
from svg.path import parse_path, Path, Move, Line, Arc, CubicBezier, QuadraticBezier


def getExtremityFromBase(topology, baseIndex):
    positions = topology.position.value
    triangles = topology.triangles.value
    nbPoints = len(positions)

    maxDistance = 0.
    extremityIndex = baseIndex

    if len(triangles) == 0 or len(positions) > 100:
        for i in range(nbPoints):
            distance = Vec3(vsub(positions[baseIndex], positions[i])).getNorm()
            if distance > maxDistance:
                maxDistance = distance
                extremityIndex = i

    return extremityIndex


def getRigidPositionsFromSVGPath(filename):
    positions = []

    if not os.path.isfile(filename):
        Sofa.msg_error("topology.py", "File does not exist : " + filename)
        return None

    file = minidom.parse(filename)
    paths = file.getElementsByTagName('path')

    for path in paths:
        segments = parse_path(path.attributes['d'].value)
        for segment in segments:
            match segment.__class__.__name__:
                case "Move":
                    q = [0., 0., -sin(pi/4), cos(pi/4)]
                    p = [0., segment.start.imag, segment.start.real]
                case "Line":
                    q = positions[-1][3:7]
                    p = [0., segment.end.imag, segment.end.real]
                case "CubicBezier":
                    c1 = np.array([0.,
                                  segment.start.imag - segment.control1.imag,
                                  segment.start.real - segment.control1.real])
                    c1 /= np.linalg.norm(c1)
                    angle = np.arctan2(c1[1], c1[2]) - pi / 2
                    q = list(Quat([0., 0., -sin(pi/4), cos(pi/4)]).rotateFromQuat(Quat([0., -sin(angle/2), 0., cos(angle/2)])))
                    p = [0., segment.start.imag, segment.start.real]
                    positions[-1] = p + q

                    c2 = np.array([0.,
                                  segment.control2.imag - segment.end.imag,
                                  segment.control2.real - segment.end.real])
                    c2 /= np.linalg.norm(c2)
                    angle = np.arctan2(c2[1], c2[2]) - pi / 2
                    q = list(Quat([0., 0., -sin(pi/4), cos(pi/4)]).rotateFromQuat(Quat([0., -sin(angle/2), 0., cos(angle/2)])))
                    p = [0., segment.end.imag, segment.end.real]
                case "QuadraticBezier":
                    Sofa.msg_error("topology.py", "Quadratic bezier curves are not handled.")
                    return None
                case "Arc":
                    Sofa.msg_error("topology.py", "Elliptic arcs are not handled.")
                    return None
                case _:
                    Sofa.msg_error("topology.py", "Error in svg file, unknown segment.")
                    return None
            positions += [p + q]

    return positions


def getIndicesInBox(positions, box):
    indicesIn = []
    indicesOut = []

    for index, pos in enumerate(positions):
        isIn = True
        for i in range(3):
            if (box[i] < box[i + 3] and (pos[i] < box[i] or pos[i] > box[i + 3])) or (box[i] > box[i + 3] and (pos[i] > box[i] or pos[i] < box[i + 3])):
                indicesOut.append(index)
                isIn = False
                break
        if isIn:
            indicesIn.append(index)

    return indicesIn, indicesOut


def applyTranslation(positions, translation):
    """

    Args:
        positions:
        translation:

    Returns:

    """
    for pos in positions:
        pos[0] += translation[0]
        pos[1] += translation[1]
        pos[2] += translation[2]


def applyRotation(positions, rotation):
    """

    Args:
        positions: list of positions
        rotation: rotation in radians

    Returns:

    """
    for pos in positions:
        q = Quat.createFromEuler(rotation)
        pos[0:3] = Vec3(pos[0:3]).rotateFromQuat(q)

        if len(pos) == 7:
            pos[3:7] = q.rotateFromQuat(Quat(pos[3:7]))


# Function used only if this script is called from a python environment
if __name__ == '__main__':
    getRigidPositionsFromSVGPath("data/meshes/redleg.svg")
