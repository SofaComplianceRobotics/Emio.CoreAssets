"""
This module defines the `Leg` class for the Emio robot. 
The `Leg` represents a deformable component with multiple configuration and modeling options.
The file `leg.py` also includes an example usage, which can be tested by running the script with the `runSofa` command:
```bash
runSofa -l SofaPython3,SofaImGui -g imgui leg.py
```
"""

import sys

import Sofa

import os.path
from math import pi, sin
import numpy as np
from scipy.linalg import logm, inv
from scipy.spatial.transform import Rotation
from splib3.numerics import Quat

from splib3.numerics import Quat, Vec3, vsub, to_radians, to_degrees
from splib3.loaders import getLoadingLocation
from utils.topology import getIndicesInBox, getRigidPositionsFromSVGPath, getExtremityFromBase
from utils.topology import applyRotation, applyTranslation
from utils import getColorFromFilename
import parameters


def _getStrainFromQuat(frame, curvAbs, gXp) -> tuple:
    """
    Thi function is used for the Cosserat model.
    It computes the strain from the current frame (quaternion). It returns the strain and the matrix gX.

    Function Arguments:
        - `frame`: current frame
        - `curvAbs`: abscissa curve
        - `gXp`: previous matrix
    """

    gX = np.zeros((4, 4), dtype=float)
    gX[0:3, 0:3] = Rotation.from_quat(frame[3:7]).as_matrix()
    gX[0:3, 3] = frame[0:3]
    gX[3, 3] = 1.

    if curvAbs <= 0.:
        xi = [0., 0., 0.]
    else:
        gXpInv = inv(gXp)
        xiHat = 1. / curvAbs * logm(np.dot(gXpInv, gX))
        xi = [xiHat[2][1], xiHat[0][2], xiHat[1][0], xiHat[0][3], xiHat[1][3], xiHat[2][3]]

    return xi[0:3], gX


class Leg(Sofa.Prefab):
    """
    The `Leg` class represents a leg component of the Emio robot. It includes rigid base, rigid extremity, 
    and deformable part, and supports multiple modeling options such as beam, cosserat, and tetra models.
    By default, the legs are added to the Emio class.

    Class Overview:
        - `base`: Represents the rigid base of the leg, typically attached to the motor.
        - `extremity`: Represents the rigid extremity part of the leg, typically attached to a connector.
        - `deformable`: Represents the deformable part of the leg.
        - `leg`: Represents the entire leg model.

    Key Features:
        - Supports multiple modeling techniques: "beam", "cosserat", and "tetra".
        - Automatically adjusts rotation and translation based on the motor position.
        - Includes visual and physical modeling components.

    Class Variables:
        - `legName` (`string`): Name of the leg, should have corresponding meshes in the "data/meshes/legs" directory.
        - `positionOnMotor` (`string`): Specifies the position on the motor. Options are: "clockwiseup", "counterclockwiseup", "clockwisedown", "counterclockwisedown"
        - `model` (`string`): Specifies the modeling technique. Options are: "beam", "cosserat", "tetra"
        - `massDensity` (`float`): Mass density of the leg material.
        - `poissonRatio` (`float`): Poisson's ratio of the leg material.
        - `youngModulus` (`float`): Young's modulus of the leg material.
        - `rotation` (`Vec3d`): Rotation of the leg.
        - `translation` (`Vec3d`): Translation of the leg.
        - `positions` (`Rigid3::VecCoord`, optional): Optional list of Rigid3 positions describing the leg's rod shape (for `beam` and `cosserat` models). If none is given, the "data/meshes/legs" directory should contain a file named "legName.txt" with the positions.
        - `crossSectionShape` (`string`): Shape of the cross-section. Options are: "circular", "rectangular"
        - `radius` (`float`): Radius of the leg, if the `crossSectionShape` is `circular` (for `beam` and `cosserat` models).
        - `thickness` (`float`): Thickness of the leg, if the `crossSection` is `rectangular` (for `beam` and `cosserat` models).
        - `width` (`float`): Width of the leg, if the `crossSection` is `rectangular` (for `beam` and `cosserat` models).

    Expected files in the "data/meshes/legs" directory:
        - legName.stl: surface mesh for the visual model. Only used for `tetra` model, for `beam` and `cosserat` models, the mesh is created from the positions.
        - legName.vtk: volume mesh for the tetra model
        - legName.txt: file containing the positions of the leg (for beam and cosserat models)

    Example Usage:
    ```python
    from utils.header import addHeader, addSolvers

    def createScene(root):
        # Header of the simulation
        settings, modelling, simulation = addHeader(root)
        addSolvers(simulation)
        # Create a leg instance
        leg = Leg(name="Leg",
                    legName="blueleg",
                    model="beam",
                    positionOnMotor="clockwiseup")
        if not leg.isValid():
            return
        simulation.addChild(leg)
    ```
    """
    prefabData = [
        {'name': 'legName', 'type': 'string', 'help': '', 'default': None},        
        {'name': 'positionOnMotor', 'type': 'string', 'help': 'clockwiseup, counterclockwiseup, clockwisedown, or counterclockwisedown', 'default': 'clockwiseup'},
        {'name': 'model', 'type': 'string', 'help': '["beam", "cosserat", "tetra"]', 'default': "beam"},
       
        {'name': 'massDensity', 'type': 'float', 'help': '', 'default': parameters.massDensity},
        {'name': 'poissonRatio', 'type': 'float', 'help': '', 'default': parameters.poissonRatio},
        {'name': 'youngModulus', 'type': 'float', 'help': '', 'default': parameters.youngModulus},
        {'name': 'rotation', 'type': 'Vec3d', 'help': '', 'default': [0.0, 0.0, 0.0]},
        {'name': 'translation', 'type': 'Vec3d', 'help': '', 'default': [0.0, 0.0, 0.0]},
       
        {'name': 'positions', 'type': 'Rigid3::VecCoord', 'help': '', 'default': None},
        {'name': 'crossSectionShape', 'type': 'string', 'help': '"circular" or "rectangular"', 'default': "rectangular"},
        {'name': 'radius', 'type': 'float', 'help': '', 'default': 5.},
        {'name': 'thickness', 'type': 'float', 'help': '', 'default': parameters.thickness},
        {'name': 'width', 'type': 'float', 'help': '', 'default': parameters.width},
    ]

    _validState = False

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

        self._addRequiredPlugins()

        self.base = self.addChild(self.name.value + 'RigidBase')
        self.extremity = self.addChild(self.name.value + 'RigidExtremity')
        self.deformable = self.addChild(self.name.value + 'DeformablePart')

        self.leg = Sofa.Core.Node("Leg")

        self.color = getColorFromFilename(self.legName.value)
        self.attachSpring = None

        i = ["clockwiseup", "counterclockwiseup", "clockwisedown", "counterclockwisedown"].index(self.positionOnMotor.value)
        rotation = [[0., 0., 0.], [0., 180., 0.], [180., 180., 0.], [180., 0., 0.]][i]
        q = Quat.createFromEuler(to_radians(self.rotation.value))
        q.rotateFromEuler(to_radians(rotation))
        self.rotation.value = to_degrees(q.getEulerAngles())

        if self._checkData():
            match self.model.value:
                case "beam":
                    self._addBeamModel()
                case "cosserat":
                    self._addCosseratModel()
                case _:
                    self._addTetraModel()
            self._addVisualModel()
            self._validState = True

        if self.positionOnMotor.value in ["clockwiseup", "clockwisedown"]:
            with self.extremity.getMechanicalState().position.writeable() as position:
                q1 = Quat(position[0][3:7])
                q2 = Quat([1., 0., 0., 0.])
                q1.rotateFromQuat(q2)
                q1.normalize()
                position[0][3:7] = q1


    def _getFilePath(self, filename) -> str:
        """
        Get the file path of the given filename in the data/meshes/legs directory.
        Returns the full path if the file exists, otherwise returns None.
        """
        
        # First check relative to the simulation file
        filePath = getLoadingLocation(os.path.dirname(os.path.abspath(sys.argv[0])) + '/data/meshes/legs/' + filename, __file__)
        if os.path.isfile(filePath):
            return filePath
            
        # Then check relative to the leg.py file
        filePath = getLoadingLocation(os.path.dirname(os.path.abspath(__file__)) + "/../data/meshes/legs/" + filename, __file__)
        if os.path.isfile(filePath):
            return filePath
        
        return None


    def _checkFile(self, filename) -> bool:
        """
        Check if the file exists in the data/meshes/legs directory.
        Returns True if it exists, False otherwise and logs an error.
        """
        if self._getFilePath(filename) is not None:
            return True
            
        Sofa.msg_error(self.getName(), f'Missing file: {filename} in data/meshes/legs directory.')
        return False
    

    def _checkData(self):
        """
        Check if the data needed to create the leg is present.
        The leg is created from a mesh, and the data should be in the data/meshes/legs directory.
        Expected files:
            - legName.stl: surface mesh for the visual model. On only used for `tetra` model, for `beam` and `cosserat` models, the mesh is created from the positions.
            - legName.vtk: volume mesh for the tetra model
            - legName.txt: file containing the positions of the leg (for beam and cosserat models)
        """

        if self.model.value in ["beam", "cosserat"]:
            if not self.positions.value.any():
                filename = self.legName.value + ".txt"
                if not self._checkFile(filename):
                    return False
                self.positions.value = np.loadtxt(self._getFilePath(filename))
                if not self.positions.value.any():
                    Sofa.msg_error(self.getName(), 'Empty positions. We cannot model the leg without a list of '
                                                'Rigid3 positions describing the curve when using the '
                                                'beam or cosserat model')
                    return False
        elif self.model.value == "tetra":
            if self.legName.value is None:
                Sofa.msg_error(self.getName(),
                               'Empty legName. We cannot model the leg with tetra without a volume mesh.')
                return False
            
            if not self._checkFile(self.legName.value + ".vtk"):
                return False
        else:
            Sofa.msg_error(self.getName(), 'Unknown model, value should be "beam", "cosserat", or "tetra".')
            return False

        filePath = self._getFilePath(self.legName.value + ".stl")
        if filePath is None:
            return False

        volume = self.addChild("Volume")
        volume.addObject("MeshSTLLoader", filename=filePath)
        volume.addObject("VolumeFromTriangles",
                         position=volume.MeshSTLLoader.position.value,
                         triangles=volume.MeshSTLLoader.triangles.value)
        volume.init()
        self.totalMass = volume.VolumeFromTriangles.volume.value * self.massDensity.value

        return True


    def _addBeamModel(self):
        """
        FEM line model from the plugin BeamAdapter.
        base, extremity, deformable
        (all parents of leg)
        """
        positions = np.copy([np.copy(pos) for pos in self.positions.value])
        applyRotation(positions, to_radians(self.rotation.value))
        applyTranslation(positions, self.translation.value)
        nbPoints = len(positions)
        nbSections = nbPoints - 1

        # The entire model
        self.leg.addObject('MeshTopology', 
                           position=[pos[0:3] for pos in positions],
                           edges=[[i, i + 1] for i in range(nbSections)])
        self.leg.addObject('MechanicalObject', template='Rigid3', position=positions)
        self.leg.addObject('BeamInterpolation', straight=False, dofsAndBeamsAligned=False,
                           crossSectionShape=self.crossSectionShape.value,
                           lengthY=self.width.value,
                           lengthZ=self.thickness.value,
                           defaultYoungModulus=self.youngModulus.value,  
                           defaultPoissonRatio=self.poissonRatio.value,
                           radius=self.radius.value)
        self.leg.addObject('AdaptiveBeamForceFieldAndMass', computeMass=True,
                           massDensity=self.massDensity.value)

        # The extremity and the base of the leg are attached to something (either the motor or a support)
        # Thus, we need to rigidify these parts.
        indicesRigidified1, indicesRigidified2, indicesDeformable, indexPairs = self._getIndicesDistribution(self.leg.MeshTopology)

        # The rigid base part
        self.base.addObject('MechanicalObject', template='Rigid3', position=positions[0])
        baseGroup = self.base.addChild("RigidifiedPoints")
        baseGroup.addObject('MechanicalObject', template='Rigid3', position=positions[indicesRigidified1],
                            showObject=False, showObjectScale=10)
        baseGroup.addObject("RigidMapping", globalToLocalCoords=True)
        baseGroup.addChild(self.leg)

        # The rigid extremity part
        self.extremity.addObject('MechanicalObject', template="Rigid3",
                                 position=positions[-1],
                                 showObject=False, showObjectScale=10)
        extremityGroup = self.extremity.addChild("ExtremityGroup")
        extremityGroup.addObject('MechanicalObject', position=positions[indicesRigidified2],
                                 template="Rigid3",
                                 showObject=False, showObjectScale=10)
        extremityGroup.addObject("RigidMapping", globalToLocalCoords=True)
        extremityGroup.addChild(self.leg)

        # The deformable part
        self.deformable.addObject('MechanicalObject', template='Rigid3', position=positions[indicesDeformable],
                                  showObject=False, showObjectScale=10)
        self.deformable.addChild(self.leg)

        # Mapping separating rigid and deformable parts
        self.leg.addObject('SubsetMultiMapping', template="Rigid3,Rigid3",
                           input=[baseGroup.getMechanicalState().linkpath,
                                  extremityGroup.getMechanicalState().linkpath,
                                  self.deformable.getMechanicalState().linkpath],
                           output=self.leg.getMechanicalState().linkpath,
                           indexPairs=indexPairs)


    def _addCosseratModel(self):
        """
        Cosserat line model from the plugin Cosserat.
        """
        nbPoints = len(self.positions)
        nbSections = nbPoints - 1
        positions = np.copy([np.copy(pos) for pos in self.positions.value])
        positions = np.flip(positions, 0)
        extremityPosition = np.copy(positions[0])
        for pos in positions:
            pos[3:7] = Quat([1., 0., 0., 0.]).rotateFromQuat(Quat(pos[3:7]))
        applyRotation(positions, to_radians(self.rotation.value))
        applyTranslation(positions, self.translation.value)

        # The entire model
        self.leg.addObject('MeshTopology', position=[pos[0:3] for pos in positions],
                           edges=[[i, i + 1] for i in range(nbSections)])
        self.leg.addObject('MechanicalObject', template='Rigid3', position=positions,
                           showObject=False, showObjectScale=10)
        self.leg.addObject("BeamInterpolation", straight=False, dofsAndBeamsAligned=False)

        # The extremity and the base of the leg are attached to something (either the motor or a support)
        # Thus, we need to rigidify these parts.
        indicesRigidified1, indicesRigidified2, indicesDeformable, indexPairs = self._getIndicesDistribution(
            self.leg.MeshTopology)

        applyRotation([extremityPosition], to_radians(self.rotation.value))
        applyTranslation([extremityPosition], self.translation.value)
        self.extremity.addObject('MechanicalObject', template='Rigid3', position=extremityPosition,
                                 showObject=False, showObjectScale=30)
        extremityGroup = self.extremity.addChild("ExtremityGroup")
        extremityGroup.addObject('MechanicalObject', template='Rigid3', position=positions[indicesRigidified2],
                                 showObject=False, showObjectScale=30)
        extremityGroup.addObject("RigidMapping", globalToLocalCoords=True)
        extremityGroup.addChild(self.leg)

        # We are now going to convert the Rigid3 orientation description to the Cosserat bending description
        # [[torsion strain, y_bending strain, z_bending strain]]
        gX = np.zeros((4, 4), dtype=float)
        gX[0:3, 0:3] = Rotation.from_quat(Quat(positions[0][3:7])).as_matrix()
        gX[0:3, 3] = positions[0][0:3]
        gX[3, 3] = 1

        lengths = []
        strain = []
        totalLength = 0
        for i in range(len(positions) - 1):
            length = Vec3(vsub(positions[i][0:3], positions[i + 1][0:3])).getNorm()
            lengths.append(length)
            totalLength += length
            xi, gX = _getStrainFromQuat(positions[i + 1], length, gX)
            strain.append(xi)

        self.deformable.addObject('MechanicalObject', position=strain)
        self.deformable.addObject('BeamHookeLawForceField',
                                  youngModulus=self.youngModulus.linkpath,
                                  poissonRatio=self.poissonRatio.linkpath,
                                  radius=self.radius.value,
                                  crossSectionShape=self.crossSectionShape.value,
                                  lengthY=self.width.linkpath,
                                  lengthZ=self.thickness.linkpath,
                                  length=lengths)
        self.deformable.addObject("FixedProjectiveConstraint",
                                  indices=[i - len(indicesRigidified2) for i in indicesRigidified1])
        self.deformable.addChild(self.leg)

        self.leg.addObject('UniformMass', totalMass=self.totalMass, showAxisSizeFactor=5)

        # Mapping separating rigid and deformable parts
        curvAbs = [0.]
        for length in lengths:
            curvAbs += [curvAbs[-1] + length]
        self.leg.addObject('DiscreteCosseratMapping',
                           curv_abs_input=curvAbs,
                           curv_abs_output=curvAbs,
                           input1=self.deformable.getMechanicalState().linkpath,
                           input2=extremityGroup.getMechanicalState().linkpath,
                           output=self.leg.linkpath,
                           debug=False, baseIndex=0)


    def _addTetraModel(self):
        """
        FEM volume model. We need a volume mesh, and we will use the component TetrahedronFEMForceField.
        """
        # The volume model
        self.leg.addObject('MeshVTKLoader',
                           filename=self._getFilePath(self.legName.value + ".vtk"),
                           rotation=self.rotation.value, translation=self.translation.value)
        self.leg.addObject('MeshTopology', src=self.leg.MeshVTKLoader.linkpath)
        self.leg.MeshTopology.init()
        self.leg.addObject('MechanicalObject', showIndices=False, showIndicesScale=0.003)
        self.leg.addObject('UniformMass', totalMass=self.totalMass)
        self.leg.addObject('TetrahedronFEMForceField',
                           poissonRatio=self.poissonRatio.linkpath,
                           youngModulus=self.youngModulus.linkpath)

        # The extremity and the base of the leg are attached to something (either the motor or a support)
        # Thus, we need to rigidify these parts.
        indicesRigidified1, indicesRigidified2, indicesDeformable, indexPairs = self._getIndicesDistribution(
            self.leg.MeshTopology)

        # The rigid base
        positions = self.leg.MeshTopology.position.value
        q = Quat.createFromEuler(to_radians(self.rotation.value))
        q.rotateFromQuat(Quat([0., 0., 0.707, 0.707]))
        q.rotateFromQuat(Quat([1., 0., 0., 0.]))
        bary = [0, 0, 0] + list(q)
        for pos in positions[indicesRigidified1]:
            for i in range(3):
                bary[i] += pos[i] / len(indicesRigidified1)
        self.base.addObject('MechanicalObject', position=bary, template='Rigid3', showObject=False, showObjectScale=20)
        baseVec3 = self.base.addChild("RigidifiedPoints")
        baseVec3.addObject('MechanicalObject', position=positions[indicesRigidified1],
                           showObject=False, showObjectScale=10, showColor=[1, 0, 0, 1])
        baseVec3.addObject("RigidMapping", globalToLocalCoords=True)
        baseVec3.addChild(self.leg)

        # The rigid extremity part
        q = Quat.createFromEuler(to_radians(self.rotation.value))
        q.rotateFromQuat(Quat([0., 0., 0.707, 0.707]))
        q.rotateFromQuat(Quat([1., 0., 0., 0.]))
        bary = [0, 0, 0] + list(q)
        for pos in positions[indicesRigidified2]:
            for i in range(3):
                bary[i] += pos[i] / len(indicesRigidified2)
        self.extremity.addObject('MechanicalObject', template="Rigid3",
                                 position=[bary],
                                 showObject=False, showObjectScale=10)
        extremityVec3 = self.extremity.addChild("ExtremityVec3")
        extremityVec3.addObject('MechanicalObject', position=positions[indicesRigidified2],
                                showObject=False, showObjectScale=10, showColor=[0, 1, 0, 1])
        extremityVec3.addObject("RigidMapping", globalToLocalCoords=True)
        extremityVec3.addChild(self.leg)

        # The deformable part
        self.deformable.addObject('MechanicalObject', position=positions[indicesDeformable],
                                  showObject=False, showObjectScale=10, showColor=[0, 0, 1, 1])
        self.deformable.addChild(self.leg)

        # Mapping separating rigid and deformable parts
        self.leg.addObject('SubsetMultiMapping', template="Vec3,Vec3",
                           input=[baseVec3.getMechanicalState().linkpath,
                                  extremityVec3.getMechanicalState().linkpath,
                                  self.deformable.getMechanicalState().linkpath],
                           output=self.leg.getMechanicalState().linkpath,
                           indexPairs=indexPairs)


    def _getIndicesDistribution(self, topology):
        """
        Get the indices of the rigidified and deformable parts of the leg.
        The rigidified parts are the base and the extremity, and the deformable part is the rest of the leg.
        The indices are used to create the mapping between the rigidified and deformable parts.
        The function also returns the index pairs for the mapping.
        """
        indicesRigidified1 = []
        indicesRigidified2 = []
        indicesDeformable = []
        positions = topology.position.value

        # First the base
        boxes = [[-10., -30., -30., 10., 30., 0.],
                 [-10., -30., -30., 10., 2., 30.]]
        for i in range(2):
            pos = [boxes[i][0:3], boxes[i][3:7]]
            applyRotation(pos, to_radians(self.rotation.value))
            boxes[i] = pos[0] + pos[1]

        for box in boxes:
            for i, t in enumerate(self.translation.value):
                box[i] += t
                box[i + 3] += t
            indR, indD = getIndicesInBox(positions=positions, box=box)
            indicesRigidified1 = list(np.unique(indicesRigidified1 + indR))
            indicesDeformable = indD if len(indicesDeformable) == 0 else np.intersect1d(indicesDeformable, indD)
        # self.leg.addObject("BoxROI", box=boxes, drawBoxes=True)
        indexExtremity = getExtremityFromBase(topology, indicesRigidified1[0])
        positionExtremity = positions[indexExtremity]

        # Second the extremity
        boxes = [[-15, -15, -15, 15, 15, 15]]
        for box in boxes:
            for i, t in enumerate(positionExtremity[0:3]):
                box[i] += t
                box[i + 3] += t
            indR, indD = getIndicesInBox(positions=positions, box=box)
            indicesRigidified2 = list(np.unique(indicesRigidified2 + indR))
            indicesDeformable = np.intersect1d(indicesDeformable, indD)
        # self.leg.addObject("BoxROI", box=boxes, drawBoxes=True)

        indexPairs = []
        incr = [0, 0, 0]
        for index in range(len(positions)):
            if index in indicesRigidified1:
                indexPairs.append([0, incr[0]])
                incr[0] += 1
            elif index in indicesRigidified2:
                indexPairs.append([1, incr[1]])
                incr[1] += 1
            else:
                indexPairs.append([2, incr[2]])
                incr[2] += 1

        assert len(indicesRigidified1) != 0, "The position of the leg seems to be incorrect."
        assert len(indicesRigidified2) != 0, "The position of the leg seems to be incorrect."
        assert len(indicesDeformable) != 0, "The position of the leg seems to be incorrect."
        return indicesRigidified1, indicesRigidified2, indicesDeformable, indexPairs


    def _addVisualModel(self):
        """
        Adds a visual model to the leg. In case of the tetra model, we need the corresponding surface mesh.
        Otherwise, the surface will be generated from the leg positions.
        """
        if self.model.value in ["tetra"]:
            visual = self.leg.addChild("Visual")
            visual.addObject("MeshSTLLoader",
                             filename=self._getFilePath(self.legName.value + ".stl"))
            visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=self.color,
                             rotation=self.rotation.value, translation=self.translation.value)
            visual.addObject('BarycentricMapping') if self.model.value == "tetra" else visual.addObject(
                'IdentityMapping')
        else:
            visual = self.leg.addChild("Visual")
            visual.addObject("MeshSTLLoader",
                             filename=self._getFilePath(self.legName.value + ".stl"))
            visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=self.color,
                             rotation=self.rotation.value, translation=self.translation.value)
            visual.addObject('SkinningMapping')


    def _addRequiredPlugins(self):
        """
        Add the RequiredPlugins of the Leg class.
        """
        plugins = self.addChild("RequiredPlugins")
        plugins.addObject('RequiredPlugin', name='Sofa.Component.IO.Mesh')
        # Needed to use components [MeshOBJLoader]
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Dynamic')
        # Needed to use components [EdgeSetTopologyContainer]
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Constant')
        # Needed to use components [MeshTopology]
        plugins.addObject('RequiredPlugin', name='Sofa.GL.Component.Rendering3D')
        # Needed to use components [OglModel]
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Topology.Container.Grid')
        # Needed to use components [RegularGridTopology]
        plugins.addObject('RequiredPlugin', name='SoftRobots')
        plugins.addObject('RequiredPlugin', name='BeamAdapter')
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Mapping.Linear')
        # Needed to use components [SubsetMultiMapping]
        plugins.addObject('RequiredPlugin', name='Cosserat')
        plugins.addObject('RequiredPlugin', name='Sofa.Component.SolidMechanics.FEM.Elastic')
        # Needed to use components [TetrahedronFEMForceField]
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Mapping.NonLinear')
        # Needed to use components [RigidMapping]
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Projective')
        plugins.addObject('RequiredPlugin', name='Sofa.Component.Engine.Generate')
        # Needed to use components [VolumeFromTriangles]


    def attachBase(self, attach, index) -> None:
        """
        Attach the base of the leg to the motor.

        Function Parameters:
            - `attach` (`Sofa.Node`): The node to which the leg's base will be attached.
            - `index` (`int`): The index of the degrees of freedom (DOFs) in the `attach` node to connect to.
        """
        if not self._validState:
            return

        base = self.leg if self.model.value == "cosserat" else self.base
        baseIndex = len(self.leg.getMechanicalState().position) - 1 if self.model.value == "cosserat" else 0

        legAttach = attach.addChild("LegAttach")
        legAttach.addObject("MechanicalObject", template="Rigid3", showObject=False, showObjectScale=10,
                            position=base.getMechanicalState().position.value[baseIndex])
        legAttach.addObject("RigidMapping", globalToLocalCoords=True, index=index)

        self._attach(part=base, attach=legAttach, indexPart=baseIndex, indexAttach=0)


    def attachExtremity(self, attach, index) -> None:
        """
        Attach the extremity of the leg to the motor.

        Function Parameters:
            - `attach` (`Sofa.Node`): The node to which the leg's extremity will be attached.
            - `index` (`int`): The index of the degrees of freedom (DOFs) in the `attach` node to connect to.
        """
        if not self._validState:
            return
        self._attach(part=self.extremity, attach=attach, indexPart=0, indexAttach=index)


    def _attach(self, part, attach, indexPart, indexAttach):
        difference = part.addChild("Difference"+str(indexAttach))
        attach.addChild(difference)
        difference.addObject("MechanicalObject", template="Rigid3", position=[[0, 0, 0, 0, 0, 0, 1]])
        self.attachSpring = difference.addObject('RestShapeSpringsForceField', points=[0],
                                                 stiffness=1e7, angularStiffness=1e14)
        difference.addObject('RigidDistanceMapping',
                             input1=part.getMechanicalState().linkpath,
                             input2=attach.getMechanicalState().linkpath,
                             output=difference.getMechanicalState().linkpath,
                             first_point=[indexPart], second_point=[indexAttach])


    def isValid(self) -> bool:
        """
        Check if the leg is in a valid state. Returns True if the leg is in a valid state, False otherwise.
        """
        return self._validState


def createScene(rootnode):
    from utils.header import addHeader, addSolvers
    from splib3.animation import AnimationManager, animate
    from parts.motor import Motor
    import argparse
    """
    Test the simulation of a single leg attached to a motor.

    Example usage:
    ```bash
    runSofa leg.py
    runSofa leg.py --argv blueleg,beam,0
    ```
    """

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Simulate a leg.')
    parser.add_argument('-n', '--name', type=str, nargs='?', help="name of the leg",
                        default='blueleg', dest="name")
    parser.add_argument('-m', '--model', type=str, nargs='?', help="name of the model",
                        choices=["cosserat", "beam", "tetra"],
                        default='beam', dest="model")
    parser.add_argument("-p", '--positionOnMotor', type=str, nargs='?', help="position on motor (clockwiseup, counterclockwiseup, clockwisedown, or counterclockwisedown)",
                        default='clockwiseup', dest="positionOnMotor")

    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    # Header of the simulation
    settings, modelling, simulation = addHeader(rootnode)
    rootnode.addObject(AnimationManager(rootnode))
    rootnode.VisualStyle.displayFlags = ["hideWireframe", "hideBehavior"]
    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)

    # Motor
    motor = Motor(name="Motor")
    simulation.addChild(motor)

    # Leg
    leg = Leg(name="Leg",
              legName=args.name,
              model=args.model,
              positionOnMotor=args.positionOnMotor
              )
    if not leg.isValid():
        return
    simulation.addChild(leg)

    # Attach the leg to motor
    leg.attachBase(motor.Parts, 1)

    # Animate the motor
    constraint = motor.addObject("JointConstraint", name="JointActuator", 
                                 minDisplacement=-pi, maxDisplacement=pi,
                                 index=0, value=0, valueType="displacement")

    def animation(target, factor):
        target.value = - sin(factor * pi * 2)

    animate(animation, {'target': constraint.value}, duration=10., mode='loop')

    return leg # used for tests
