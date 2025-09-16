import sys
import os

import Part
import FreeCAD

import argparse
import breptosurfacemesh as toSurfaceMesh
import breptovolumemesh as toVolumeMesh

import numpy as np
from math import pi
from scipy.spatial.transform import Rotation

filedirpath = os.path.dirname(os.path.abspath(__file__)) + "/../data/meshes/legs/"


def discretizeAndSaveRigidFrames(filename, curve, nbPoints, pulleyRadius):

    # We improve the discretization of the curve
    spline = None
    for geometry in curve.Geometry:
        if type(geometry) == Part.BSplineCurve:
            spline = geometry

    if spline is None:
        print("[discretizeAndSaveRigidFrames][ERROR] Couldn't find B-Spline in the Sketch.")
        return

    frames = np.empty((0, 7))
    frames = np.append(frames, [[0., -pulleyRadius, 0., -0.5, -0.5, -0.5, 0.5]], 0)
    for param in np.linspace(spline.FirstParameter, spline.LastParameter, nbPoints):
        point, tangentVector = spline.getD1(param)  # returns point and tangent vector
        # Build a local frame based on the tangent vector. The direction of tangent vector is the x-axis
        # of the new frame to follow the convention of beams.
        # Orientation
        theta = np.arctan2(tangentVector[1], tangentVector[0]) - pi/2.
        # this gives the angular displacement of the local

        # Rotate
        point = Rotation.from_euler('y', -pi/2.).apply(point)
        quaternion = Rotation.from_euler('z', -pi/2).inv() * Rotation.from_euler('y', theta) * Rotation.from_euler('x', pi)
        quaternion = quaternion.as_quat()

        # Frame = Position + Orientation
        frame = np.append(np.array(point), quaternion)
        # Collect Frames in an array
        frames = np.append(frames, [frame], 0)

    np.savetxt(filename, frames)


def freecadCurveToBrepFile(thickness, width, size, cadName="leg-cad", legName='myleg', fromFreeCAD=True):
    # We load the freecad project,
    if not fromFreeCAD:
        filename = filedirpath + cadName + ".FCStd"
        doc = FreeCAD.openDocument(filename)
    else:
        doc = FreeCAD.ActiveDocument
    pulleyRadius = 22.5

    # and get the leg sketch.
    curve = doc.getObjectsByLabel(legName + "Sketch")[0]
    discretizeAndSaveRigidFrames(filedirpath + legName + ".txt", curve, int(3./size), pulleyRadius)

    # Generate the meshes for 3D FEM
    # We create the profile of the leg,
    profile = doc.addObject("Sketcher::SketchObject", "Profile")
    profile.addGeometry(Part.LineSegment(FreeCAD.Vector(0., thickness / 2. - pulleyRadius, 0.),
                                         FreeCAD.Vector(0., -thickness / 2. - pulleyRadius, 0.)))

    # make the sweep,
    sweep = doc.addObject('Part::Sweep', 'Sweep')
    sweep.Sections = [profile]
    sweep.Spine = curve
    sweep.Solid = False
    sweep.Frenet = False
    doc.recompute()  # compute the sweep

    # and finally extrude. (Note: we use this two steps method because the sweep doesn't seem to
    # work when the profile is out of the path plane. The problem only occurs in the python script,
    # it works fine from the GUI)
    legvolume = sweep.Shape.extrude(FreeCAD.Vector(0, 0, width))
    legvolume.Placement = FreeCAD.Placement(FreeCAD.Vector(width / 2, 0, 0),
                                            FreeCAD.Rotation(FreeCAD.Vector(0, 1, 0), -90),  # Rotate to match the motor
                                            FreeCAD.Vector(0, 0, 0))

    # Make the union with the part to attach the leg on the motor
    attach = doc.getObjectsByLabel("attachmotor")[0]
    legvolume = legvolume.fuse(attach.Shape)

    # We export the result into a file.brep. We will use gmsh to generate the surface and volume meshes
    # suitable for the simulations.
    legvolume.exportBrep(filedirpath + legName + '.brep')

    # Clear document
    doc.removeObject('Sweep')
    doc.removeObject('Profile')


def freecadCurveToMeshes(thickness, width, size, cadName="leg-cad", legName='myleg', fromFreeCAD=True, display=False):
    freecadCurveToBrepFile(thickness, width, size, cadName, legName, fromFreeCAD)

    toSurfaceMesh.generateMeshAndExport("legs/" + legName, size, display)
    toVolumeMesh.generateMeshAndExport("legs/" + legName, size, display)


if __name__ == '__main__':
    """ FreeCAD Bezier Curve To Meshes
     With this file you can generate the meshes needed to simulate the leg with a 2D and 3D finite element models.
     The meshes are generated from a 2D curve designed with FreeCAD. You will need to provide the FreeCAD project.
     The cad file should be in the 'data' directory. The resulting meshes will be added to the 'data/meshes/legs' repository
    """

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Generates meshes to simulate 3D finite element models, from '
                                                 'a 2D curve designed with FreeCAD.')
    parser.add_argument("-c", "--cadName", help='FreeCAD project name', default='cad',
                        type=str, nargs='?', dest='cadName')
    parser.add_argument("-l", "--legName", help="leg's sketch name in the FreeCAD project, should be 'legName'Sketch.",
                        default='myleg', type=str, nargs='?', dest="legName")
    parser.add_argument('-t', '--thickness', help='thickness of the leg in mm', default=5,
                        type=int, nargs='?', dest="thickness")
    parser.add_argument('-w', '--width', help='width of the leg in mm', default=10,
                        type=int, nargs='?', dest="width")
    parser.add_argument("-s", "--sizeFactor",
                        type=float, nargs='?', help='Mesh size factor', default=0.3, dest='meshSizeFactor')
    parser.add_argument("-d", "--display", action='store_true', help='Open gmsh GUI to see the mesh',
                        dest='display')

    args = parser.parse_args()
    freecadCurveToMeshes(args.thickness, args.width, args.meshSizeFactor, args.cadName, args.legName, False, args.display)
