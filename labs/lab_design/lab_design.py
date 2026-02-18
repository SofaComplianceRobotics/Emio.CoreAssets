import os
import sys
import Sofa

from splib3.numerics import Vec3, vsub

from emio.utils.header import addHeader, addSolvers
from emio.parts.emio import Emio, getParserArgs
from emio.parts.controllers.assemblycontroller import AssemblyController
from emio.parts.gripper import Gripper
from emio.parts.centerpart import CenterPart

import Sofa.ImGui as MyGui


class LabGUI(Sofa.Core.Controller):
    
    def __init__(self, emio, type):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUI"

        self.root = emio.getRoot()
        self.target = self.root.Modelling.Target.getMechanicalState()
        if type == "deformable":
            self.effector = emio.centerpart.part.Effector.getMechanicalState()
        else:
            self.effector = emio.centerpart.Effector.getMechanicalState()
        self.error = self.root.addData(name="error", type="double", value=0)

        MyGui.PlottingWindow.addData(" effector error (mm)", self.error)

    def onAnimateBeginEvent(self, e):

        self.error.value = Vec3(vsub(self.target.position.value[0][0:3], self.effector.position.value[0][0:3])).getNorm()


def createScene(rootnode):

    import argparse
    import emio.parameters as parameters

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='')
    parser.add_argument(metavar='centerPartType', type=str, nargs='?',
                        help="type of the center part (either deformable or rigid)",
                        default='rigid', dest="centerPartType")
    parser.add_argument('--no-connection', dest="connection", action='store_false',
                        help="use when you want to run the simulation without the robot")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    settings, modelling, simulation = addHeader(rootnode, inverse=True)

    rootnode.dt = 0.05
    rootnode.gravity = [0., 9810., 0.]
    addSolvers(simulation)
    rootnode.VisualStyle.displayFlags.value = ["hideBehavior"]

    # Add Emio to the scene
    emio = Emio(name="Emio",
                legsName=["myleg"],
                legsModel=["beam"],
                legsPositionOnMotor=["counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown"],
                centerPartName="mygripper",
                centerPartType=args.centerPartType,
                centerPartModel="tetra",
                centerPartClass=CenterPart if args.centerPartType == "rigid" else Gripper,
                centerPartYoungModulus=parameters.youngModulus*parameters.tetraYMFactor,
                # parameters.youngModulus has been measured for the beam models. In the labs, a factor 'parameters.tetraYMFactor'
                # is applied when using the tetra model (because of the artificial rigidity introduced by the mesh discretization).
                extended=True
                )
    simulation.addChild(emio)
    emio.attachCenterPartToLegs()
    emio.addObject(AssemblyController(emio))

    # Effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1] * 4)
    emio.effector.addObject("RigidMapping", rigidIndexPerPoint=[0, 1, 2, 3] if args.centerPartType != "rigid" else [0, 0, 0, 0])

    # Target
    effectorTarget = modelling.addChild('Target')
    effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    effectorTarget.addObject('MechanicalObject', template='Rigid3',
                             position=[0, -150, 0, 0, 0, 0, 1],
                             showObject=True, showObjectScale=20)

    # Inverse components and GUI elements
    emio.addInverseComponentAndGUI(effectorTarget.getMechanicalState().position.linkpath,
                                   barycentric=(args.centerPartType != "rigid"))
    if args.centerPartType != "rigid":
        TCP = modelling.addChild("TCP")
        TCP.addObject("MechanicalObject", template="Rigid3", position=emio.effector.EffectorCoord.barycenter.linkpath)
        MyGui.setIPController(rootnode.Modelling.Target, TCP, rootnode.ConstraintSolver)


    rootnode.addObject(LabGUI(emio, args.centerPartType))

    MyGui.ProgramWindow.importProgram(os.path.dirname(__file__)+"/mypickandplace.crprog")
    MyGui.MoveWindow.setTCPLimits(-100, 100,
                                  emio.motors[0].JointActuator.minAngle.value,
                                  emio.motors[0].JointActuator.maxAngle.value)
    if args.centerPartType == "deformable":
        MyGui.MoveWindow.addAccessory("Gripper's opening (mm)", emio.centerpart.part.Effector.Distance.DistanceMapping.restLengths, 5, 70)
        MyGui.ProgramWindow.addGripper(emio.centerpart.part.Effector.Distance.DistanceMapping.restLengths, 5, 70)

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()