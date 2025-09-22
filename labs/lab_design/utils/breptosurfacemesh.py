import sys
import gmsh
import os
import argparse


def generateMeshAndExport(filename, meshSizeFactor, display):
    # Before using any functions in the Python API, Gmsh must be initialized:
    gmsh.initialize()
    gmsh.option.setNumber("General.Verbosity", 0)

    dirpath = os.path.dirname(os.path.abspath(__file__)) + "/../data/meshes/"

    # First, we load the step file
    gmsh.model.occ.importShapes(dirpath + filename + '.brep')
    gmsh.model.occ.synchronize()

    # We choose the size factor for the discretion of the meshes
    gmsh.option.setNumber("Mesh.MeshSizeFactor", meshSizeFactor)

    # Here we generate the surface mesh and export it to a stl file
    gmsh.model.mesh.generate(2)
    gmsh.write(dirpath + filename + '.stl')

    # To visualize the model we can run the GUI
    if display:
        gmsh.fltk.run()

    # This should be called when you are done using the Gmsh Python API
    gmsh.finalize()


if __name__ == '__main__':
    """ Mesh Generation
     Generates a 2D mesh (triangles) from a ".brep" file given by argument. 
     The given mesh filename should be in the 'data/meshes/' directory. The generated meshes will be added to the same
     directory.
    """

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Generates a 2D mesh (triangles) from a ".brep" file.')
    parser.add_argument(type=str, nargs='?',
                        help='File name (without extension) that should be found in the "data/meshes/" directory',
                        default=None, dest='filename')
    parser.add_argument("-s", "--sizefactor",
                        type=float, nargs='?', help='Mesh size factor', default=1, dest='meshSizeFactor')
    parser.add_argument("-d", "--display", action='store_true', help='Open gmsh GUI to see the mesh',
                        dest='display')

    args = parser.parse_args()

    if args.filename is None:
        print("[Error] a file name (without extension) should be given as argument. The corresponding '.brep' file "
              "should be found in the 'data/meshes/' directory.")
        sys.exit()

    generateMeshAndExport(args.filename, args.meshSizeFactor, args.display)
