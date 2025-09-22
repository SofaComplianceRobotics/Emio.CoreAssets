import sys
import os

import FreeCAD
import Part

import argparse
import breptosurfacemesh as toSurfaceMesh
import breptovolumemesh as toVolumeMesh

filedirpath = os.path.dirname(os.path.abspath(__file__)) + "/../data/meshes/centerparts/"


def freecadGripperToBrepFile(thickness, angle, cadName, partName, fromFreeCAD):
    # We load the freecad project,
    if not fromFreeCAD:
        filename = filedirpath + cadName + ".FCStd"
        doc = FreeCAD.openDocument(filename)
    else:
        doc = FreeCAD.ActiveDocument

    # and get the leg sketch.

    if thickness > 9:
        thickness = 9
    if thickness < 1:
        thickness = 1

    dx = (9 - thickness) / 2
    doc.getObject('Sketch003').setDatum(39, FreeCAD.Units.Quantity(str(dx) + ' mm'))
    doc.getObject('Extrude006').LengthFwd = str(thickness) + ' mm'

    doc.Box.Placement = FreeCAD.Placement(FreeCAD.Vector(-5, 5, 22),
                                          FreeCAD.Rotation(FreeCAD.Vector(1, 0, 0), angle),
                                          FreeCAD.Vector(0, 0, 0))

    doc.recompute()
    Part.export([doc.getObject("Fusion014")], filedirpath + partName + '.brep')


def freecadGripperToMeshes(thickness, angle, size, cadName="gripper-cad", partName='mygripper', display=False, fromFreeCAD=True):
    freecadGripperToBrepFile(thickness, angle, cadName, partName, fromFreeCAD)
    toSurfaceMesh.generateMeshAndExport("centerparts/" + partName, size, display)
    toVolumeMesh.generateMeshAndExport("centerparts/" + partName, size, display)


if __name__ == '__main__':
    """ FreeCAD Gripper To Meshes
     With this file you can generate the meshes needed to simulate the gripper.
    """

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='')
    parser.add_argument("-c", "--cadName", help='FreeCAD project name', default='cad',
                        type=str, nargs='?', dest='cadName')
    parser.add_argument('-t', '--thickness', help='thickness of the circle in mm, must be in [1,9[', default=3,
                        type=float, nargs='?', dest="thickness")
    parser.add_argument('-a', '--angle', help='fingers opening in degree', default=20,
                        type=float, nargs='?', dest="angle")
    parser.add_argument("-s", "--sizeFactor",
                        type=float, nargs='?', help='Mesh size factor', default=0.3, dest='meshSizeFactor')
    parser.add_argument("-d", "--display", action='store_true', help='Open gmsh GUI to see the mesh',
                        dest='display')

    args = parser.parse_args()
    freecadGripperToMeshes(thickness=args.thickness, angle=args.angle, size=args.sizeFactor, cadName=args.cadName,
                           display=args.display, fromFreeCAD=False)

