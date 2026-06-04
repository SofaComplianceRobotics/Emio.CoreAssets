import numpy as np
from math import pi
from splib3.numerics import Vec3, vsub

from emio.utils import getListFromArgs
from emio.utils.header import addHeader, addSolvers
from emio import Emio, getParserArgs
from emio.parts.controllers.assemblycontroller import AssemblyController
from emio.parts.controllers.trackercontroller import DotTracker
import emio.parameters as parameters

import Sofa.SoftRobotsInverse
import Sofa.ImGui as MyGui

import myQP_lab_inversekinematics as myQP


class LabGUIExerciseDirect(Sofa.Core.Controller):

    def __init__(self, root, emio):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUIExerciseDirect"
        self.root = root
        self.emio = emio

        # Move Tab
        MyGui.MoveWindow.setActuators([motor.JointActuator.value for motor in emio.motors], [0, 0, 0, 0],
                                      "displacement")
        MyGui.MoveWindow.setActuatorsLimits(-pi, pi)

    def onAnimateBeginEvent(self, e):
        for leg in self.emio.legs:
            if "TetrahedronFEMForceField" in leg.leg.forceField.getValueString():
                leg.leg.TetrahedronFEMForceField.reinit()
            elif "BeamHookeLawForceField" in leg.deformable.forceField.getValueString():
                leg.deformable.BeamHookeLawForceField.reinit()
            else:
                leg.leg.BeamInterpolation.defaultYoungModulus = [leg.youngModulus.value]
                leg.leg.BeamInterpolation.reinit()


class LabGUIExerciseIK(Sofa.Core.Controller):

    def __init__(self, root, emio):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUIExerciseIK"
        self.root = root

        MyGui.setIPController(root.Modelling.Target, emio.effector, root.ConstraintSolver)

        # Move Tab
        MyGui.MoveWindow.setTCPLimits(-40, 40,
                                      emio.motors[0].JointActuator.minAngle.value,
                                      emio.motors[0].JointActuator.maxAngle.value)
        MyGui.MoveWindow.setActuatorsDescription("Motors Position (rad)")
        MyGui.MoveWindow.setActuators([motor.JointActuator.angle for motor in emio.motors],
                                      [0, 1, 2, 3], "displacement")
        MyGui.MoveWindow.setActuatorsLimits(emio.motors[0].JointActuator.minAngle.value,
                                            emio.motors[0].JointActuator.maxAngle.value)


class LabGUICamera(Sofa.Core.Controller):

    def __init__(self, markers, root):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUICamera"
        self.root = root
        self.markers = markers

        # My Robot Tab
        MyGui.MyRobotWindow.addInformation("Error marker", markers.error)

        # My Plotting Tab
        MyGui.PlottingWindow.addData("marker tracker error", self.markers.error)

        self.markersInitDone = False

    def onAnimateBeginEvent(self, e):

        if self.root.getChild("DepthCamera") is not None:
            # Compute simulation to real error
            trackers = self.root.DepthCamera.Trackers.position.value
            markers = self.markers.getMechanicalState().position.value

            if len(trackers) >= 1:
                self.markers.error.value = Vec3(vsub(trackers[0][0:3], markers[0][0:3])).getNorm()


class MyQPInverseProblemSolver(Sofa.SoftRobotsInverse.QPInverseProblemSolver):

    def __init__(self, emio, sensor, target, effector, getTorques, *args, **kwargs):
        Sofa.SoftRobotsInverse.QPInverseProblemSolver.__init__(self, *args, **kwargs)
        self.name = "ConstraintSolver"

        self.emio = emio
        self.sensor = sensor
        self.target = target.getMechanicalState()
        self.effector = effector.getMechanicalState()

        self.assembly = emio.addObject(AssemblyController(emio))
        self.getTorques = getTorques
        self.lastTorques = None

    def solveSystem(self):
        W = self.W()
        dfree = self.dfree()
        torques = self.lambda_force()  # pointer on lambda

        iE = [4, 5, 6]
        iA = [0, 1, 2, 3]

        Hdq_free = np.copy(dfree)
        # We remove the displacement from the free motion vector to let the student implement this part
        # based on the course content
        q_a=[self.emio.motors[i].JointActuator.angle.value for i in range(4)]
        Hdq_free[iA] -= q_a
        # q_e - q_t is also removed, but directly from the PositionEffector component

        if self.assembly.done:
            try:
                torques[iA] = self.getTorques(W=W, 
                                              Hdq_free=Hdq_free,
                                              iE=iE, 
                                              iA=iA,
                                              q_s=self.sensor.position.value[0][0:3],
                                              q_t=self.target.position.value[0][0:3],
                                              q_e=self.effector.position.value[0][0:3],
                                              q_a=q_a)
            except:
                torques[iA] = np.copy(self.lastTorques)
                return True

        self.lastTorques = np.copy(torques[iA])
        return True


def createScene(rootnode):
    args = getParserArgs()
    exercise1 = ("blueleg-direct" in args.legsName)
    exercise2 = (args.legsName[0] == "blueleg")
    exercise3 = (args.legsName[0] == "whiteleg")

    settings, modelling, simulation = addHeader(rootnode, inverse=(not exercise1))

    rootnode.dt = 0.03
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)
    rootnode.VisualStyle.displayFlags.value = ["hideBehavior"]

    # Add Emio to the scene
    emio = Emio(name="Emio",
                legsName=["blueleg"] if exercise1 else getListFromArgs(args.legsName),
                legsModel=getListFromArgs(args.legsModel),
                legsPositionOnMotor=getListFromArgs(args.legsPositionOnMotor),
                legsYoungModulus=[parameters.youngModulus*parameters.tetraYMFactor] if args.legsModel[0] == "tetra" else [parameters.youngModulus],
                # parameters.youngModulus has been measured for the beam models. In the labs, a factor of 'parameters.tetraYMFactor'
                # is applied when using the tetra model (because of the artificial rigidity introduced by the mesh discretization).
                centerPartName=args.centerPartName,
                centerPartType="rigid",
                extended=True)
    simulation.addChild(emio)
    emio.attachCenterPartToLegs()

    # Effector
    effector = emio.effector
    effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1])
    effector.addObject("RigidMapping", index=0)

    effectorTarget = None
    if not exercise1:
        # Target
        effectorTarget = modelling.addChild('Target')
        effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
        effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
        effectorTarget.addObject('MechanicalObject', template='Rigid3',
                                 position=[0, -130 if exercise3 else -170, 0, 0, 0, 0, 1],
                                 showObject=True, showObjectScale=20)

    # Add RealSense camera tracker
    sensor = emio.effector.getMechanicalState()
    if args.connection and not exercise1:

        # Add Markers
        markers = emio.CenterPart.Effector.addChild("Markers")
        markers.addObject("MechanicalObject",
                          position=[[0, -5, 0]] if "blue" in args.centerPartName else [[0, 0, 0]],
                          showObject=True, showObjectScale=7, drawMode=1, showColor=[1, 0, 0, 1])
        markers.addObject("RigidMapping")
        markers.addData(name="error", type="float", value=0)

        try:
            dotTracker = rootnode.addObject(DotTracker(name="DotTracker",
                                                       root=rootnode,
                                                       nb_tracker=1,
                                                       show_video_feed=False,
                                                       track_colors=True,
                                                       comp_point_cloud=False,
                                                       scale=1))
            sensor = dotTracker.mo
        except RuntimeError:
            Sofa.msg_error(__file__, "Camera not detected")

    if exercise1:
        emio.addObject(AssemblyController(emio))
        for motor in emio.motors:
            motor.addObject("JointConstraint", name="JointActuator", 
                            minDisplacement=-pi, maxDisplacement=pi,
                            index=0, value=0, valueType="displacement")
        rootnode.addObject(LabGUIExerciseDirect(rootnode, emio))  # Set up customized GUI for exercise 1
    elif exercise2:
        # Let's implement and try our own solver
        rootnode.removeObject(rootnode.ConstraintSolver)
        rootnode.addObject(MyQPInverseProblemSolver(emio, sensor, effectorTarget, effector, myQP.getTorques))
        # Inverse components and GUI elements
        emio.addInverseComponentAndGUI(targetMechaLink=effector.getMechanicalState().position.linkpath, withGUI=False) 
        # We set the target to follow the position of the effector to let the student implement this part
        rootnode.addObject(LabGUIExerciseIK(rootnode, emio))  # Set up customized GUI for exercise 2
        if args.connection:
            rootnode.addObject(LabGUICamera(markers, rootnode))  # Set up customized GUI for trackers
    elif exercise3:
        # Inverse components and GUI elements
        emio.addInverseComponentAndGUI(targetMechaLink=effectorTarget.getMechanicalState().position.linkpath, 
                                       orientationWeight=0, withGUI=True)
        rootnode.addObject(LabGUIExerciseIK(rootnode, emio))  # Set up customized GUI for exercise 3
        if args.connection:
            rootnode.addObject(LabGUICamera(markers, rootnode))  # Set up customized GUI for trackers
    
    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()

    return exercise1, exercise2, exercise3 # used for tests
