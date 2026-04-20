import Sofa
import numpy as np

from emio.parts.centerpart import CenterPart
from emio.utils.topology import getExtremityFromBase
import emio.parameters as parameters

from splib3.numerics import Quat, Vec3
from splib3.loaders import getLoadingLocation
from math import pi, cos, sin, floor


class Gripper(CenterPart):

    prefabData = CenterPart.prefabData + [
        {'name': 'radius', 'type': 'double', 'help': '', 'default': 26.5},
        {'name': 'thickness', 'type': 'double', 'help': 'thickness of the ring', 'default': 3},
        {'name': 'angle', 'type': 'double', 'help': 'opening angle in radian', 'default': pi/3.27},
        {'name': 'nbSections', 'type': 'int', 'help': '', 'default': 20}
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.effector = None

    def _addDeformableCenterPart(self):
        match self.model.value:
            case "tetra":
                super()._addDeformableCenterPart()
            case _:
                positions = []
                edges1 = []
                edges2 = []
                nbSections = self.nbSections.value
                indices = [int(nbSections / 4) * i for i in range(4)]

                attachposition = self._params["attachPositionInLocalCoord"]
                if self.flip:  # the legs are pointing upward, we flip the center part
                    for pos in attachposition:
                        pos[3:7] = Quat.createFromAxisAngle([0., 0., 1.], pi).rotateFromQuat(Quat(pos[3:7]))
                    temp = attachposition[1][3:7]
                    attachposition[1][3:7] = attachposition[3][3:7]
                    attachposition[3][3:7] = temp

                # Ring
                for i in range(nbSections):
                    theta = 2 * pi / nbSections * i + pi / 2.
                    positions += [[self.radius.value * sin(theta), -self.thickness.value / 2., self.radius.value * cos(theta),
                                   0., sin(theta/2.), 0., cos(theta/2.)]]
                    edges1 += [[i, i+1]]
                edges1[-1][1] = 0

                # Fingers
                nbSections = int(nbSections / 2.)
                for j in range(2):
                    index = [indices[-1], indices[1]][j]
                    q1 = Quat(positions[index][3:7])
                    q2 = Quat.createFromAxisAngle([0., 0., 1.], -pi/2.)
                    q3 = Quat.createFromAxisAngle([0., 1., 0.], -self.angle.value)
                    q1 = q1.rotateFromQuat(q2).rotateFromQuat(q3)
                    edges2 += [[index, nbSections * (2 + j)]]
                    for i in range(nbSections):
                        p = np.copy(positions[index])
                        p[1] -= 50./nbSections * i + 23
                        p[2] -= [13, -13][j]
                        p[3:7] = q1
                        q = Quat.createFromAxisAngle([1., 0., 0.], [-1., 1.][j] * self.angle.value)
                        p[0:3] = Vec3(p[0:3]).rotateFromQuat(q)
                        positions += [p]
                        if i < nbSections - 1:
                            edges2 += [[nbSections * (2 + j) + i, nbSections * (2 + j) + i + 1]]

                nbAttach = 4

                # Attach (only for visualization)
                for j in range(nbAttach):
                    index = indices[j]

                    q1 = Quat(positions[index][3:7])
                    q2 = Quat.createFromAxisAngle([0., 0., 1.], pi / 2.)
                    q1 = q1.rotateFromQuat(q2)
                    # TODO: debug the vibration when using DOF0TransformNode0
                    # DOF0TransformNode0[-nbAttach + j][3:7] = q1

                    edges2 += [[index, self.nbSections.value * 2 + j]]
                    p = np.copy(positions[index])
                    p[1] += 15
                    p[3:7] = q1
                    positions += [p]

                # Entire object
                self.addObject('MechanicalObject', template="Rigid3", position=positions,
                               showObject=False, showObjectScale=1, showIndices=False, showIndicesScale=0.01)
                mass = self.addChild("ComputeMass")
                mass.addObject("MeshSTLLoader", filename=self._getFilePath(self.partName.value + ".stl"))
                mass.addObject('VolumeFromTriangles',
                               position=mass.MeshSTLLoader.position.value,
                               triangles=mass.MeshSTLLoader.triangles.value)
                mass.VolumeFromTriangles.init()
                self.addObject('UniformMass', totalMass=mass.VolumeFromTriangles.volume.value * self.massDensity.value)

                for i in range(2):
                    if i == 0:
                        DOF0TransformNode0 = [[0., 0., 0., 0., 0., 0., 1.] for i in range(nbSections + nbAttach)]
                        DOF1TransformNode1 = [[0., 0., 0., 0., 0., 0., 1.] for i in range(nbSections + nbAttach)]
                    else:
                        DOF0TransformNode0 = [[0., 0., 0., 0., 0., 0., 1.] for i in range(nbSections * 2)]
                        DOF1TransformNode1 = [[0., 0., 0., 0., 0., 0., 1.] for i in range(nbSections * 2)]
                        index = [indices[-1], indices[1]][i]
                        q1 = Quat(positions[index][3:7])
                        q2 = Quat.createFromAxisAngle([0., 0., 1.], pi / 2.)
                        q3 = Quat.createFromAxisAngle([0., 1., 0.], self.angle.value)
                        q1 = q1.rotateFromQuat(q2).rotateFromQuat(q3)
                        DOF0TransformNode0[0] = [0., 0., 0.] + list(q1)
                        DOF0TransformNode0[nbSections] = [0., 0., 0.] + list(q1)

                    part = self.addChild(["Ring", "Fingers"][i])
                    part.addObject("MeshTopology", position=[pos[0:3] for pos in positions], edges=[edges1, edges2][i])
                    part.addObject('BeamInterpolation', straight=False, dofsAndBeamsAligned=False,
                                   crossSectionShape="rectangular",
                                   lengthY=[self.thickness.value, 10][i],
                                   lengthZ=[self.thickness.value, 5][i],
                                   defaultYoungModulus=self.youngModulus.value,
                                   defaultPoissonRatio=self.poissonRatio.value,
                                   DOF0TransformNode0=DOF0TransformNode0,
                                   DOF1TransformNode1=DOF1TransformNode1,
                                   topology=part.MeshTopology.linkpath,
                                   )
                    part.addObject('AdaptiveBeamForceFieldAndMass', computeMass=True,
                                   massDensity=self.massDensity.value)

                # Attach
                self.attach = self.addChild("LegsAttach")
                self.attach.addObject("MechanicalObject", template="Rigid3", position=attachposition,
                                      showObject=False, showObjectScale=10, showIndices=False, showIndicesScale=0.2)
                self.attach.addObject("RigidMapping",
                                      rigidIndexPerPoint=[indices[-1], indices[0], indices[1], indices[2]],
                                      globalToLocalCoords=True)

    def _addVisualModel(self):
        match self.model.value:
            case "tetra":
                super()._addVisualModel()
            case _:
                visual = self.addChild("Visual")
                visual.addObject("MeshSTLLoader", filename=self._getFilePath(self.partName.value + ".stl"), rotation=self.rotation)
                visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=self.color.value)
                visual.addObject("SkinningMapping")

    def addGripperEffector(self):
        match self.model.value:
            case "tetra":
                topology = self.part.getTopology()
                indicesRigidified, _, _ = self._getIndicesDistribution(topology)
                indexFinger1 = getExtremityFromBase(topology, indicesRigidified[0][0])
                indexFinger2 = getExtremityFromBase(topology, indicesRigidified[2][0])
                self.effector = self.part.addChild("Effector")
                self.effector.addObject("MeshTopology",
                                        position=[topology.position.value[indexFinger1],
                                                  topology.position.value[indexFinger2]], edges=[[0, 1]])
                self.effector.addObject("MechanicalObject", showObject=False, showObjectScale=2, drawMode=2)
                self.effector.addObject("BarycentricMapping")
            case _:
                p1 = Vec3(0., -50., 0.)
                p1.rotateFromAxisAngle([-1., 0., 0.], self.angle.value)
                p2 = Vec3(0., -50., 0.)
                p2.rotateFromAxisAngle([-1., 0., 0.], self.angle.value)
                self.effector = self.addChild("Effector")
                self.effector.addObject("MeshTopology",
                                        position=[p1, p2], edges=[[0, 1]])
                self.effector.addObject("MechanicalObject", showObject=False, showObjectScale=5, drawMode=2)
                self.effector.addObject("RigidMapping", rigidIndexPerPoint=[int(self.nbSections.value/4), int(self.nbSections.value/4) * 3])

        distance = self.effector.addChild("Distance")
        distance.addObject("MechanicalObject", template="Vec1")
        distance.addObject("PositionEffector", template="Vec1", indices=[0], effectorGoal=[0])
        distance.addObject("DistanceMapping",
                           mapForces=False,
                           topology=self.effector.MeshTopology.linkpath, restLengths=[35])

    def addCollision(self, group=""):
        collision = None
        if self.model.value == "tetra":
            collision = self.part.addChild("CollisionModel")
        else:
            collision = self.addChild("CollisionModel")
        collision.addObject("MeshSTLLoader",
                            filename=self._getFilePath(self.partName + "collision.stl"))
        collision.addObject("MeshTopology", src=collision.MeshSTLLoader.linkpath)
        collision.addObject("MechanicalObject")
        collision.addObject("PointCollisionModel", group=group)
        collision.addObject("LineCollisionModel", group=group)
        collision.addObject("TriangleCollisionModel", group=group)

        if self.model.value == "tetra":
            collision.addObject("BarycentricMapping")
        else:
            collision.addObject("SkinningMapping")


def createScene(rootnode):
    import emio.utils as utils
    from emio.utils.header import addHeader, addSolvers
    
    import sys
    import argparse

    inverse = False

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Simulate the centerpart.')
    parser.add_argument(metavar='centerPartName', type=str, nargs='?',
                        help="name of the center part (ex: yellowpart, bluepart)",
                        default='whitepart', dest="centerPartName")
    parser.add_argument(metavar='centerPartType', type=str, nargs='?',
                        help="type of the center part (either deformable or rigid)",
                        default='deformable', dest="centerPartType")

    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    settings, modelling, simulation = addHeader(rootnode, inverse=inverse)
    settings.addObject('RequiredPlugin', pluginName='Sofa.Component.Constraint.Projective')
    rootnode.addObject("VisualStyle", displayFlags=["showWireframe", "showBehavior"])

    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)

    gripper = Gripper(name="Gripper",
                      partName=args.centerPartName,
                      type=args.centerPartType,
                      color=utils.RGBAColor.white
                      )
    simulation.addChild(gripper)

    if inverse:
        rootnode.ConstraintSolver.epsilon.value = 1
        gripper.addGripperEffector()
        gripper.attach.addObject("FixedProjectiveConstraint", indices=[1, 3])
        gripper.attach.addObject("PartialFixedProjectiveConstraint", indices=[0, 2], fixedDirections=[1, 0, 1, 1, 1, 1])
        for i in [0, 2]:
            gripper.attach.addObject("SlidingActuator", template="Rigid3", indices=i, direction=[0, 1, 0, 0, 0, 0],
                                     maxPositiveDisp=15, maxNegativeDisp=15)
    else:
        from splib3.animation import animate, AnimationManager
        rootnode.addObject(AnimationManager(rootnode))
        
        def animation(target, factor, index, direction, startTime):
            if factor > 0:
                position = np.copy(target.rest_position.value)
                position[index][1] = 10 * direction * factor
                target.rest_position.value = position

        for i in range(4):
            attach = gripper.LegsAttach
            attach.addObject("RestShapeSpringsForceField", points=[0, 1, 2, 3], angularStiffness=1e12, stiffness=1e12)
            animate(animation, {'target': attach.getMechanicalState(),
                                'index': i,
                                'direction': [-1, 1, -1, 1][i],
                                'startTime': 0
                                },
                    duration=0.5,
                    mode='pingpong')
