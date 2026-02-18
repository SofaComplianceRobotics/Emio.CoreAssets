import os
import numpy as np

import Sofa
import Sofa.SofaConstraintSolver  
import Sofa.SoftRobotsInverse
import Sofa.ImGui as MyGui

from emio.parts.controllers.assemblycontroller import AssemblyController
from emio.parts.controllers.trackercontroller import DotTracker

import myQP_lab_closedloop as myQP
import myControl as myControl


class MyQPInverseProblemSolver(Sofa.SoftRobotsInverse.QPInverseProblemSolver):

    def __init__(self, emio, sensor, target, effector, *args, **kwargs):
        Sofa.SoftRobotsInverse.QPInverseProblemSolver.__init__(self, *args, **kwargs)
        self.name = "ConstraintSolver"

        self.sensor = sensor
        self.target = target
        self.effector = effector

        self.assembly = emio.addObject(AssemblyController(emio))

    def solveSystem(self):
        W = self.W()
        dfree = self.dfree()
        torques = self.lambda_force()  # pointer on lambda

        iE = [4, 5, 6]
        iA = [0, 1, 2, 3]
        dq_free = np.copy(dfree)

        if self.assembly.done:
            try:
                torques[iA] = myQP.getTorques(W, dq_free, iE, iA,
                                              self.sensor.position.value[0][0:3],
                                              self.target.position.value[0][0:3],
                                              self.effector.position.value[0][0:3])
            except Exception as e:
                Sofa.msg_error(os.path.basename(__file__), str(e))

        return True


class MyController(Sofa.Core.Controller):

    def readTuningParameters(self):
        return [p.value for p in self.paramsData]

    def createParameters(self):
        params = myControl.initParameters()
        n = len(params)
        for i in range(n):
            datafield = self.addData(name=params[i][3], type="float", value=params[i][0])
            self.paramsData.append(datafield)
            MyGui.MyRobotWindow.addSettingInGroup(params[i][3],
                                                  datafield,
                                                  params[i][1],
                                                  params[i][2],
                                                  "Controller Parameters")

    def __init__(self, qptarget, effector, dt, assembly, usertarget, sensor, *args, **kwargs):
        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.assembly = assembly
        self.qptarget = qptarget
        self.effector = effector
        self.usertarget = usertarget
        self.dt = dt.value

        self.sensor = sensor
        self.sensor_offset = np.array([0., 0, 0])
        self.state = self.effector.MechanicalObject.position.value.copy()[0][0:3]

        self.paramsData = []
        self.createParameters()

        # flag to know if the control should start
        self.started = False

        self.addData(name="error", type="float", value=0)
        self.addData(name="errorX", type="float", value=0)
        self.addData(name="errorY", type="float", value=0)
        self.addData(name="errorZ", type="float", value=0)

        self.addData(name="stateX", type="float", value=0)
        self.addData(name="stateY", type="float", value=0)
        self.addData(name="stateZ", type="float", value=0)

        MyGui.PlottingWindow.addData("error", self.error)
        MyGui.PlottingWindow.addData("errorX", self.errorX)
        MyGui.PlottingWindow.addData("errorY", self.errorY)
        MyGui.PlottingWindow.addData("errorZ", self.errorZ)

        MyGui.PlottingWindow.addData("stateX", self.stateX)
        MyGui.PlottingWindow.addData("stateY", self.stateY)
        MyGui.PlottingWindow.addData("stateZ", self.stateZ)

    def onAnimateBeginEvent(self, _):  # called at each begin of animation step
        # gather the required datas
        sim_effector_position = self.effector.MechanicalObject.position.value.copy()[0][0:3]

        robot_effector_position = self.sensor.position[0][0:3] + self.sensor_offset

        if MyGui.getRobotConnectionToggle():
            effector_position = robot_effector_position
        else:
            effector_position = sim_effector_position

        reference = self.usertarget.MechanicalObject.position[0][0:3]

        error = reference - effector_position
        # to show the value on the interface (graphs)
        self.error.value = np.linalg.norm(error)
        self.errorX.value = error[0]
        self.errorY.value = error[1]
        self.errorZ.value = error[2]

        self.stateX.value = self.state[0]
        self.stateY.value = self.state[1]
        self.stateZ.value = self.state[2]

        state = self.state

        target_qat = self.qptarget.getMechanicalState().position[0][3:7]
        dt = self.dt

        # check if assembly is done
        if self.assembly.done and not self.started:
            param = self.readTuningParameters()
            self.state = myControl.init_control_state(sim_effector_position, effector_position, reference, state, param, dt, )
            self.started = True

        if self.started:
            param = self.readTuningParameters()
            req_position, state = myControl.update_control(sim_effector_position, effector_position, reference, state, param, dt, )
            self.qptarget.getMechanicalState().position = [np.hstack([req_position, target_qat])]
            self.state = state


def createScene(rootnode):
    from emio.utils.header import addHeader, addSolvers
    from emio import Emio, getParserArgs
    import Sofa.ImGui as MyGui

    args = getParserArgs()

    settings, modelling, simulation = addHeader(rootnode, inverse=True)
    addSolvers(simulation, rayleighMass=0.)

    rootnode.dt = 0.0333
    rootnode.gravity = [0., -9810., 0.]
    rootnode.VisualStyle.displayFlags.value = ["showInteractionForceFields"]

    # Add Emio to the scene
    emio = Emio(name="Emio",
                legsName=["blueleg"],
                legsModel=["beam"],
                legsPositionOnMotor=["counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown"],
                centerPartName="bluepart",
                centerPartType="rigid",
                extended=True)
    if not emio.isValid():
        return

    simulation.addChild(emio)
    emio.attachCenterPartToLegs()

    # Add effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, -5.0, 0, 0, 0, 0, 1],
                            showObject=True, showObjectScale=20)
    emio.effector.addObject("RigidMapping", index=0)

    # Target
    QPEffectorTarget = modelling.addChild('Target')
    QPEffectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    QPEffectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    QPEffectorTargetMo = QPEffectorTarget.addObject('MechanicalObject', template='Rigid3',
                                                    position=[0, -140, 00, 0, 0, 0, 1],
                                                    showObject=True, showObjectScale=20)

    # User Target
    UserEffectorTarget = modelling.addChild('User Target')
    UserEffectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    UserEffectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    UserEffectorTarget.addObject('MechanicalObject', template='Rigid3',
                                              position=[0, -140, 00, 0, 0, 0, 1],
                                              showObject=True, showObjectScale=20)

    # Add RealSense camera tracker
    sensor = emio.effector.getMechanicalState()
    if args.connection:
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

    # Let's implement and try our own solver
    rootnode.removeObject(rootnode.ConstraintSolver)
    rootnode.addObject(MyQPInverseProblemSolver(emio, sensor, QPEffectorTargetMo, emio.effector.getMechanicalState()))

    # Add the closed loop controller
    emio.addObject(MyController(QPEffectorTarget,
                                emio.effector, rootnode.dt,
                                emio.AssemblyController, UserEffectorTarget, sensor))

    # Inverse components and GUI
    emio.addInverseComponentAndGUI(emio.effector.getMechanicalState().position.linkpath, withGUI=True)
    MyGui.setIPController(UserEffectorTarget, emio.effector, rootnode.ConstraintSolver)

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()

    return rootnode
