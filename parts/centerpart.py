"""
This module defines the `CenterPart` class for the Emio robot.
By default this example will load the white part (deformable gripper).
The file `centerpart.py` also contains an example, try it by running the script with the runSofa command:
```bash
runSofa -l SofaPython3,SofaImGui -g imgui centerpart.py
```
"""
import Sofa
import os, sys
import numpy as np
from math import pi
import json
from splib3.loaders import getLoadingLocation
from splib3.numerics import Quat
from utils.topology import getIndicesInBox
import parameters


class CenterPart(Sofa.Prefab):
    """
    Represents the center part of the Emio robot that connected the legs together (also called connector).
    
    Class Variables:
        - `partName` (`string`): Name of the center part (e.g., "whitepart", "yellowpart", "bluepart"), should have corresponding meshes in the "data/meshes/centerparts" directory.
        - `type` (`string`): Type of the center part, either "deformable" or "rigid".
        - `model` (`string`): Model type between "tetra" and "beam", if deformable.
        - `massDensity` (`float`): Mass density of the center part.
        - `poissonRatio` (`float`): Poisson's ratio of the material, if deformable.
        - `youngModulus` (`float`): Young's modulus of the material, if deformable.
        - `color` (`Vec4d`): Color of the center part, for rendering.
        - `rotation` (`Vec3d`): Rotation of the center part in degrees.

    Class Members:
        - `attach`: Node containing the positions to attach the legs.
        - `deformable`: Node containing the deformable part, if deformable.

    Expected files in the "data/meshes/centerparts" directory:
        - partName.stl: surface mesh for the visual model. 
        - partName.vtk: volume mesh for the tetra model.
        - partName.json: file containing the initial position of the center part and the position of the legs'attach in local coordinates.

    Example Usage:
    ```python
    from centerpart import CenterPart
    from utils import addHeader, addSolvers
    def createScene(root):
        settings, modelling, simulation = addHeader(root)
        addSolvers(simulation)

        centerpart = root.addChild(CenterPart(name="CenterPart",
                                             partName="whitepart",
                                             type="deformable",
                                             color=[1, 1, 1, 1]))
    ```
    """
    prefabData = [
        {'name': 'positions', 'type': 'Rigid3::VecCoord', 'help': '', 'default': None},
        {'name': 'partName', 'type': 'string', 'help': '', 'default': None},
        {'name': 'model', 'type': 'string', 'help': 'model between tetra and beam', 'default': 'beam'},
        {'name': 'type', 'type': 'string', 'help': '["deformable", "rigid"]', 'default': "deformable"},
        {'name': 'massDensity', 'type': 'float', 'help': '', 'default': parameters.massDensity},
        {'name': 'poissonRatio', 'type': 'float', 'help': '', 'default': parameters.poissonRatio},
        {'name': 'youngModulus', 'type': 'float', 'help': '', 'default': parameters.youngModulus}, 
        {'name': 'color', 'type': 'Vec4d', 'help': '', 'default': [1, 1, 1, 1]},
        {'name': 'rotation', 'type': 'Vec3d', 'help': '', 'default': [0, 0, 0]}
    ]


    def _getFilePath(self, filename) -> str:
        """
        Get the file path of the given filename in the data/meshes/centerparts directory.
        Returns the full path if the file exists, otherwise returns None.
        """
 
        # First check relative to the simulation file
        filePath = getLoadingLocation(os.path.dirname(os.path.abspath(sys.argv[0])) + '/data/meshes/centerparts/' + filename, __file__)
        if os.path.isfile(filePath):
            return filePath
            
        # Then check relative to the centerpart.py file
        filePath = getLoadingLocation(os.path.dirname(os.path.abspath(__file__)) + "/../data/meshes/centerparts/" + filename, __file__)
        if os.path.isfile(filePath):
            return filePath
            
        return None


    def _checkFile(self, filename) -> bool:
        """
        Check if the file exists in the data/meshes/centerparts directory.
        Returns True if it exists, False otherwise and logs an error.
        """
        if self._getFilePath(filename) is not None:
            return True
            
        Sofa.msg_error(self.getName(), f'Missing file: {filename} in data/meshes/centerparts directory.')
        return False
    
    
    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

        self._addRequiredPlugins()

        filename = self.partName.value + '.json'
        self._checkFile(filename)
        self._params = json.load(open(self._getFilePath(filename)))

        self.flip = False
        if self.rotation[0] == 180:  # the legs are pointing upward, we flip the center part
            self.flip = True

        self._checkFile(self.partName.value + '.stl')
        match self.type.value:
            case "deformable":
                self._addDeformableCenterPart()
            case "rigid":
                self._addRigidCenterPart()
            case _:
                Sofa.msg_error("centerpart.py", 'Unknown model, value should be "deformable", or "rigid".')
                return

        self._addVisualModel()


    def _addDeformableCenterPart(self):
        """
        Add a deformable center part to the simulation.
        The part is created using a tetrahedral mesh loaded from a VTK file. The mass density, Poisson's ratio, and Young's modulus
        are set based on the parameters provided. The part is then attached to the legs using a rigid mapping.
        """
        self._checkFile(self.partName.value + '.vtk')

        # Load the mesh and create the topology, mechanical object, mass and force field
        # This node contains the entire object
        part = Sofa.Core.Node("EntireObject")
        part.addObject("MeshVTKLoader", filename=self._getFilePath(self.partName.value + ".vtk"), rotation=self.rotation)
        part.addObject("MeshTopology", src=part.MeshVTKLoader.linkpath)
        part.addObject('MechanicalObject')
        mass = part.addChild("ComputeMass")
        mass.addObject('VolumeFromTetrahedrons',
                       position=part.MeshVTKLoader.position.value,
                       tetras=part.MeshVTKLoader.tetras.value)
        mass.VolumeFromTetrahedrons.init()
        part.addObject('UniformMass', totalMass=mass.VolumeFromTetrahedrons.volume.value * self.massDensity.value)
        part.addObject("TetrahedronFEMForceField", youngModulus=self.youngModulus.value, poissonRatio=self.poissonRatio.value)
        self.part = part

        # Get the indices of the rigidified and deformable parts (attach to legs)
        indicesRigidified, indicesDeformable, indexPairs = self._getIndicesDistribution(part.MeshTopology)

        # Node containing the rigidified part to attach the legs
        self.attach = self.addChild("LegsAttach")
        attachposition = self._params["attachPositionInLocalCoord"]
        if self.flip:  # the legs are pointing upward, we flip the center part
            for pos in attachposition:
                pos[3:7] = Quat.createFromAxisAngle([0., 0., 1.], pi).rotateFromQuat(Quat(pos[3:7]))
            temp = attachposition[1][3:7]
            attachposition[1][3:7] = attachposition[3][3:7]
            attachposition[3][3:7] = temp
        self.attach.addObject("MechanicalObject", template="Rigid3", position=attachposition,
                              showObject=False, showObjectScale=10, showIndices=False, showIndicesScale=0.02)

        rigidifiedPositions = []
        rigidIndexPerPoint = []
        for index in range(len(part.MeshTopology.position)):
            for i, indices in enumerate(indicesRigidified):
                if index in indices:
                    rigidifiedPositions += [part.MeshTopology.position[index]]
                    rigidIndexPerPoint += [i]
        rigidVec3 = self.attach.addChild("Vec3")
        rigidVec3.addObject("MechanicalObject", position=rigidifiedPositions,
                            showObject=False, showObjectScale=1, drawMode=2, showColor=[0, 1, 0, 1])
        rigidVec3.addObject("RigidMapping", rigidIndexPerPoint=rigidIndexPerPoint, globalToLocalCoords=True)
        rigidVec3.addChild(part)

        # Node containing the deformable part
        self.deformable = self.addChild("DeformablePart")
        self.deformable.addObject("MechanicalObject", position=part.MeshTopology.position.value[indicesDeformable],
                                  showObject=False, showObjectScale=1, drawMode=2, showColor=[1, 0, 0, 1])
        self.deformable.addChild(part)

        # Mapping used to separate the rigidified and deformable parts
        part.addObject('SubsetMultiMapping', template="Vec3,Vec3",
                       input=[rigidVec3.getMechanicalState().linkpath,
                              self.deformable.getMechanicalState().linkpath],
                       output=part.getMechanicalState().linkpath,
                       indexPairs=indexPairs)

    def _addRigidCenterPart(self):
        """
        Add a rigid center part to the simulation.
        """

        # Load the mesh and create the topology, mechanical object, and mass
        self.addObject('MechanicalObject', template='Rigid3', position=self._params["initialPosition"],
                       showObject=False, showObjectScale=20,
                       rotation=self.rotation)
        mass = self.addChild("ComputeMass")
        mass.addObject("MeshSTLLoader", filename=self._getFilePath(self.partName.value + ".stl"))
        mass.addObject('GenerateRigidMass', src=mass.MeshSTLLoader.linkpath, density=self.massDensity.value)
        self.addObject('UniformMass', vertexMass=mass.GenerateRigidMass.rigidMass.linkpath)

        # This node contains the positions to attach the legs
        self.attach = self.addChild("LegsAttach")
        attachposition = self._params["attachPositionInLocalCoord"]
        if self.flip:  # the legs are pointing upward, we flip the center part
            temp = attachposition[1]
            attachposition[1] = attachposition[3]
            attachposition[3] = temp
        self.attach.addObject("MechanicalObject", position=attachposition, template="Rigid3",
                              showObject=False, showObjectScale=10, showIndices=False, showIndicesScale=0.02)
        self.attach.addObject("RigidMapping", globalToLocalCoords=False)

    def _getIndicesDistribution(self, topology):
        """
        Get the indices of the rigidified and deformable parts based on the attachment positions.
        The rigidified parts are the ones that are attached to the legs, while the deformable parts are the rest.
        Also create the index pairs for the mapping between the rigidified and deformable parts.
        """
        indicesRigidified = []
        indicesDeformable = []
        positions = topology.position.value

        attachposition = self._params["attachPositionInLocalCoord"]
        if self.flip:  # the legs are pointing upward, we flip the center part
            for pos in attachposition:
                pos[1] = -pos[1]

        for k in range(4):
            box = [-5., -5., -5., 5., 5., 5.]
            for i in range(3):
                box[i] += attachposition[k][i]
                box[i + 3] += attachposition[k][i]

            indR, indD = getIndicesInBox(positions=positions, box=box)
            indicesRigidified += [indR]
            indicesDeformable = indD if len(indicesDeformable) == 0 else np.intersect1d(indicesDeformable, indD)

        indexPairs = []
        incr = [0, 0]
        for index in range(len(positions)):
            for k in range(4):
                if index in indicesRigidified[k]:
                    indexPairs.append([0, incr[0]])
                    incr[0] += 1
            if index in indicesDeformable:
                indexPairs.append([1, incr[1]])
                incr[1] += 1

        return indicesRigidified, indicesDeformable, indexPairs

    def _addVisualModel(self):
        """
        Add the visual model of the center part to the simulation.
        The visual model is created using a mesh loaded from an STL file. The color of the model is set based on the parameters provided.
        The visual model is added to the appropriate node based on the type of center part (deformable or rigid).
        """
        match self.type.value:
            case "rigid":
                visual = self.addChild("Visual")
                visual.addObject("MeshSTLLoader", filename=self._getFilePath(self.partName.value + ".stl"))
                visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=self.color.value)
                visual.addObject('RigidMapping')
            case _:
                visual = self.part.addChild("Visual")
                visual.addObject("MeshSTLLoader", filename=self._getFilePath(self.partName.value + ".stl"), rotation=self.rotation)
                visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=self.color.value)
                visual.addObject("BarycentricMapping")

    def _addRequiredPlugins(self):
        plugins = self.addChild("RequiredPlugins")
        plugins.addObject('RequiredPlugin', 
                          pluginName=['Sofa.Component.Topology.Container.Constant' # Needed to use components [MeshTopology]
                                      ,'Sofa.Component.Topology.Container.Grid' # Needed to use components [RegularGridTopology]
                                      ,'Sofa.GL.Component.Rendering3D' # Needed to use components [OglModel]
                                      ,'Sofa.Component.Engine.Generate' # Needed to use components [GenerateRigidMass]
                                      ,'Sofa.Component.Mapping.Linear' # Needed to use components [BarycentricMapping,SubsetMultiMapping]  
                                      ,'Sofa.Component.Mapping.NonLinear' # Needed to use components [RigidMapping]  
                                      ,'Sofa.Component.Mass' # Needed to use components [UniformMass]  
                                      ,'Sofa.Component.SolidMechanics.FEM.Elastic' # Needed to use components [TetrahedronFEMForceField]
                                    ])
        



def createScene(rootnode):
    import utils
    import sys
    from utils.header import addHeader, addSolvers
    import argparse

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Simulate the centerpart.')
    parser.add_argument(metavar='centerPartName', type=str, nargs='?',
                        help="name of the center part (ex: whitepart, yellowpart, bluepart)",
                        default='whitepart', dest="centerPartName")
    parser.add_argument(metavar='centerPartType', type=str, nargs='?',
                        help="type of the center part (either deformable or rigid)",
                        default='deformable', dest="centerPartType")

    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    settings, modelling, simulation = addHeader(rootnode)
    settings.addObject('RequiredPlugin', pluginName='Sofa.Component.Constraint.Projective')

    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)

    centerpart = CenterPart(name="CenterPart",
                            partName=args.centerPartName,
                            type=args.centerPartType,
                            color=utils.RGBAColor.lightblue if "blue" in args.centerPartName else utils.getColorFromFilename(args.centerPartName)
                            )
    simulation.addChild(centerpart)
    centerpart.attach.addObject("FixedProjectiveConstraint", indices=[0])

