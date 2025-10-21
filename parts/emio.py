"""
This module defines the `Emio` class, which represents the Emio robot.
The `Emio` class builds the robot's structure, including its motors, legs, and center part, and provides methods for adding components and GUI elements.
The file `emio.py` also contains an example usage. You can test it by running the script with the runSofa command:
```bash
runSofa -l SofaPython3,SofaImGui -g imgui emio.py
```
"""

from math import sin, cos, pi

from splib3.numerics import to_radians
from splib3.loaders import getLoadingLocation
from parts.motor import Motor
from parts.leg import Leg
from parts.centerpart import CenterPart
from parts.gripper import Gripper
from parts.camera import Camera
from utils.topology import applyTranslation, applyRotation
from utils import getListFromArgs, getColorFromFilename, RGBAColor

import Sofa.Core
import Sofa.ImGui as MyGui
import Sofa.SofaConstraintSolver
import parameters


class EmioGUI(Sofa.Core.Controller):
    """
    The `EmioGUI` class setups the elements of the graphical user interface for SOFA robotics.
    It uses a user-friendly interface to control the Emio robot's parameters and visualize its state.
    The GUI includes windows for robot settings, movement controls, and plotting.

    Class Variables:
        - `emio`: The Emio robot instance.
        - `plotTorquesAngles`: A boolean flag to enable or disable torque and angle plotting.

    Requirements:
        - This class requires inverse components to be added to the Emio instance.
        - The instance of Emio should be added in the graph scene before creating the GUI: to allow the GUI to control the robot, EmioGUI must access the inverse solver which is located at the root of the scene.
        - The instance of Emio should also have the effector and actuator components added: typically done by calling the `addInverseComponentAndGUI` method. 
        
    Elements added to the GUI:
        - My Robot: Allows users to adjust robot settings such as maximum speed and motor angle limits.
        - Move: Provides controls for moving the robot's TCP and adjusting motor angles.
        - Plotting: Visualizes torque and angle data for each motor.
    """

    def __init__(self, emio, plotTorquesAngles=False):
        Sofa.Core.Controller.__init__(self)
        self.name = "EmioGUI"
        root = emio.getRoot()
        self.guiActuators = [0, 0, 0, 0]

        MyGui.setIPController(root.Modelling.Target, emio.effector, root.ConstraintSolver)

        # Simulation State Tab
        MyGui.SimulationState.addData("TCP", "Frame", emio.effector.getMechanicalState().position)
        for i in range(emio.nbLegs.value):
            MyGui.SimulationState.addData("Torques", "M" + str(i), emio.motors[i].JointActuator.effort)
        for i in range(emio.nbLegs.value):
            MyGui.SimulationState.addData("Angles", "M" + str(i), emio.motors[i].JointActuator.angle)

        # My Robot Tab
        MyGui.MyRobotWindow.addSetting("Max TCP speed (mm/s)", emio.effector.EffectorCoord.maxSpeed, 0, 2000)
        for i, leg in enumerate(emio.legs):
            if (leg is not None):
                group = "M" + str(i)
                MyGui.MyRobotWindow.addSettingInGroup("Min angle (rad)", emio.motors[i].JointActuator.minAngle, -pi, 0, group)
                MyGui.MyRobotWindow.addSettingInGroup("Max angle (rad)", emio.motors[i].JointActuator.maxAngle, 0, pi, group)

        # Move Tab
        MyGui.MoveWindow.setTCPLimits(-40, 40,
                                      emio.motors[0].JointActuator.minAngle.value,
                                      emio.motors[0].JointActuator.maxAngle.value)
        MyGui.MoveWindow.setActuatorsDescription("Motors Position (rad)")
        MyGui.MoveWindow.setActuators([emio.motors[i].JointActuator.angle for i in range(len(emio.motors))],
                                      [0, 1, 2, 3], "displacement")
        for i in range(len(emio.motors)):
            MyGui.MoveWindow.setActuatorLimits(i, emio.motors[i].JointActuator.minAngle.value,
                                               emio.motors[i].JointActuator.maxAngle.value)

        # Plotting Tab
        if plotTorquesAngles:
            for i in range(len(emio.motors)):
                MyGui.PlottingWindow.addData(" torque M" + str(i) + " 1e-3Nmm ", emio.motors[i].JointActuator.effort)
                MyGui.PlottingWindow.addData(" angle M" + str(i) + " (rad) ", emio.motors[i].JointActuator.angle)


class Emio(Sofa.Prefab):
    """
    The `Emio` class represents the Emio robot in the simulation. It constructs the robot's structure, including its motors, legs, and center part, and provides methods for adding components to solve the inverse kinematics and integrate GUI elements.

    Class Variables:
        - `legsName` (`list[str]`): A list of names for the legs, corresponding to the mesh file names in the "data/meshes/legs" directory. The order follows the numbering of the motors. For a single type of leg, use a list like `["blueleg"]`. To skip a leg, use `"None"` as the name, e.g., `["blueleg", "blueleg", None, None]`.
        - `legsPositionOnMotor` (`list[str]`): A list of positions for each leg on the motor. Possible values are "clockwiseup", "counterclockwiseup", "clockwisedown", or "counterclockwisedown".
        - `legsModel` (`list[str]`): A list of models for each leg. Possible values are "beam", "cosserat", or "tetra".
        - `legsMassDensity` (`list[float]`): A list of mass densities for each leg. At least one value is expected, which will be applied to all legs in that case.
        - `legsPoissonRatio` (`list[float]`): A list of Poisson ratios for each leg. At least one value is expected, which will be applied to all legs in that case.
        - `legsYoungModulus` (`list[float]`): A list of Young's moduli for each leg. At least one value is expected, which will be applied to all legs in that case.
        - `centerPartName` (`str`): The name of the center part, which should correspond to the mesh file name in the "data/meshes/centerparts" directory.
        - `centerPartType` (`str`): The type of the center part. Possible values are "deformable", "rigid", or "gripper".
        - `centerPartModel` (`str`): The model of the center part. Possible values are "beam" or "tetra".
        - `centerPartMassDensity` (`float`): The mass density of the center part material.
        - `centerPartPoissonRatio` (`float`): The Poisson ratio of the center part material, if deformable.
        - `centerPartYoungModulus` (`float`): The Young's modulus of the center part material, if deformable.
        - `extended` (`bool`): A flag indicating whether the robot is in extended mode (True) or compact mode (False).
        - `platformLevel` (`int`): The level of the platform. Possible values are 0, 1, or 2.
        - `motorsDistanceToCenter` (`list[float]`): A list of distances from the motors to the center part. The default value is [97.5, 97.5, 97.5, 97.5] which correspond to the real device.
    
    Class Members:
        - `motors`: A list of motor objects.
        - `legs`: A list of leg objects.
        - `centerpart`: The center part object.
        - `effector`: The effector node, which is used for inverse kinematics.

    Example Usage:
    ```python
    from emio import Emio
    from utils import addHeader, addSolvers

    def createScene(root):
        settings, modelling, simulation = addHeader(root)
        addSolvers(simulation)

        emio = Emio(name="Emio", 
                    legsName=["blueleg"], 
                    centerPartName="yellowpart", 
                    centerPartType="rigid")
        if not emio.isValid():
            return
        simulation.addChild(emio)
        emio.attachCenterPartToLegs()
    ```
    """
    prefabData = [
        {'name': 'legsName', 'type': 'vector<string>', 
         'help': 'The name of the legs, which should correspond to the name of the mesh files, ex: ["blueleg"]. \
                  For a setup with different legs, give a list of names for motor n0 to n4, ex ["blueleg", "whiteleg", "blueleg", "blueleg"]. \
                  To skip a leg give "None" as a name, ["blueleg", "None", "blueleg", "None"]', 
         'default': ['blueleg']},
        {'name': 'legsPositionOnMotor', 'type': 'vector<string>', 'help': 'clockwiseup, counterclockwiseup, clockwisedown, or counterclockwisedown',
         'default': ["clockwiseup"]},
        {'name': 'legsModel', 'type': 'vector<string>', 'help': '["beam", "cosserat", "tetra"]', 'default': ["beam"]},
        {'name': 'legsMassDensity', 'type': 'vector<float>', 'help': 'List of mass density for each leg. At least one value is expected (applied to all legs in that case).', 'default': [parameters.massDensity]},
        {'name': 'legsPoissonRatio', 'type': 'vector<float>', 'help': 'List of Poisson ratio for each leg. At least one value is expected (applied to all legs in that case).', 'default': [parameters.poissonRatio]},
        {'name': 'legsYoungModulus', 'type': 'vector<float>', 'help': 'List of Young modulus for each leg. At least one value is expected (applied to all legs in that case).', 'default': [parameters.youngModulus]},
        {'name': 'centerPartName', 'type': 'string', 'help': '', 'default': None},
        {'name': 'centerPartType', 'type': 'string', 'help': '["deformable", "rigid", "gripper"]', 'default': 'rigid'},
        {'name': 'centerPartModel', 'type': 'string', 'help': 'if deformable, model between tetra and beam', 'default': 'beam'},
        {'name': 'centerPartMassDensity', 'type': 'float', 'help': 'if deformable, mass density of the material', 'default': parameters.massDensity},
        {'name': 'centerPartPoissonRatio', 'type': 'float', 'help': 'if deformable, Poisson ratio of the material', 'default': parameters.poissonRatio},
        {'name': 'centerPartYoungModulus', 'type': 'float', 'help': 'if deformable, Young modulus of the material', 'default': parameters.youngModulus},
        {'name': 'extended', 'type': 'bool', 'help': '', 'default': False},
        {'name': 'platformLevel', 'type': 'int', 'help': '0, 1, or 2', 'default': 0},
        {'name': 'motorsDistanceToCenter', 'type': 'vector<double>', 'help': '', 'default': [100, 100, 100, 100]},
    ]

    _validState = True

    def __init__(self, centerPartClass=CenterPart, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

        self._centerPartClass = centerPartClass
        self.addData(name="nbLegs", type="int", value=4)
        centerPartPositions = []

        # Add motors and legs
        self.motors = []
        self.legs = []
        distances = self.motorsDistanceToCenter.value
        legsPositionOnMotor = self.legsPositionOnMotor.value
        legsModel = self.legsModel.value
        legsMassDensity = self.legsMassDensity.value
        legsYoungModulus = self.legsYoungModulus.value
        legsPoissonRatio = self.legsPoissonRatio.value

        assert len(legsPositionOnMotor) > 0, "At least one position is expected"
        assert len(legsModel) > 0, "At least one model is expected"
        assert len(legsMassDensity) > 0, "At least one mass density is expected"
        assert len(legsYoungModulus) > 0, "At least one Young's modulus is expected"
        assert len(legsPoissonRatio) > 0, "At least one Poisson's ratio is expected"

        for i in range(self.nbLegs.value):
            angle = 2. * pi / self.nbLegs.value * i

            radius = distances[i] if i < len(distances) else distances[0]
            translation = [radius * sin(angle), 0, radius * cos(angle)]
            rotation = [0., angle*360./(2.*pi) + 180. * (i%2+1), 0.] # the motors are rotated to match the real device (facing each other)

            # Motor
            motor = Motor(name="Motor" + str(i), translation=translation, rotation=rotation,
                          tempvisurotation=[[-90, 90][i % 2], 180, 0], color=[0., 0., 0., 0.])
            self.addChild(motor)
            self.motors.append(motor)

            if (i < len(self.legsName.value) and self.legsName.value[i] == "None"):
                self.legs.append(None)
            else:
                # Leg
                positionOnMotor = legsPositionOnMotor[i] if i < len(legsPositionOnMotor) else legsPositionOnMotor[0]
                model = legsModel[i] if i < len(legsModel) else legsModel[0]
                leg = Leg(name="Leg" + str(i),
                        legName=self.legsName.value[i] if i < len(self.legsName.value) else self.legsName.value[0],
                        positionOnMotor=positionOnMotor,
                        model=model,
                        translation=translation, rotation=rotation,
                        massDensity=legsMassDensity[i] if i < len(legsMassDensity) else legsMassDensity[0],
                        poissonRatio=legsPoissonRatio[i] if i < len(legsPoissonRatio) else legsPoissonRatio[0],
                        youngModulus=legsYoungModulus[i] if i < len(legsYoungModulus) else legsYoungModulus[0]
                        )
                self.legs.append(leg)
                if not leg.isValid():
                    self._validState = False
                    Sofa.msg_error(self.getName(), "At least one leg is not valid, cannot create Emio.")
                    break
                else:
                    self.addChild(leg)
                    # Attach leg to motor
                    leg.attachBase(motor.Parts, 1)

                    # Store leg extremity's position to define the center part of the robot
                    position = list(leg.extremity.getMechanicalState().position.value[0])
                    applyRotation([position], to_radians(rotation))
                    applyTranslation([position], translation)
                    centerPartPositions += [position]

        # Robot's center part
        if self._validState:
            if self.centerPartName.value is not None and self.centerPartName.value != "None":
                color = getColorFromFilename(self.centerPartName.value) if "blue" not in self.centerPartName.value else RGBAColor.lightblue
                self.centerpart = centerPartClass(name="CenterPart",
                                                positions=centerPartPositions,
                                                partName=self.centerPartName.value,
                                                model=self.centerPartModel.value,
                                                massDensity=self.centerPartMassDensity.value,
                                                poissonRatio=self.centerPartPoissonRatio.value,
                                                youngModulus=self.centerPartYoungModulus.value,
                                                type=self.centerPartType.value,
                                                color=color,
                                                rotation=[0, 0, 0] if "down" in legsPositionOnMotor[0] else [180, 180, 0]
                                                )
                if self.centerPartType.value == "rigid":
                    self.effector = self.centerpart.addChild("Effector")
                else:
                    self.effector = self.centerpart.attach.addChild("Effector")
                self.addChild(self.centerpart)
            self._addBox()
            self._addCamera()

    def _addBox(self):
        """
        Adds the structure of the robot to the simulation (only for visual rendering).
        """
        box = self.addChild("Box")
        if self.extended.value:
            box.addObject("MeshSTLLoader", filename=getLoadingLocation("../data/meshes/base-extended.stl", __file__))
            self._addPlatform()
        else:
            box.addObject("MeshSTLLoader", filename=getLoadingLocation("../data/meshes/base-compact.stl", __file__))
        box.addObject("OglModel", src=box.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.05])

    def _addPlatform(self):
        """
        Adds the platform to the simulation (only for visual rendering).
        """
        platform = self.addChild("Platform")
        platform.addObject("MeshSTLLoader", filename=getLoadingLocation("../data/meshes/supports/platform.stl", __file__),
                           translation=[0, [0, 35, 70][self.platformLevel.value], 0])
        platform.addObject("OglModel", src=platform.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.1])

    def _addCamera(self):
        """
        Adds the camera to the simulation (for visual rendering and access the sim to real transformations).
        """
        self.addChild(Camera(extended=self.extended.value))

    def attachCenterPartToLegs(self) -> None:
        """
        Attaches the center part to the legs.
        The center part is attached to the legs at their extremities.
        The legs are attached to the motors at their base.
        """
        if not self._validState:
            Sofa.msg_error(self.getName(),
                           "Emio has not been correctly initialized, cannot attach the center part to the legs.")
            return

        for i, leg in enumerate(self.legs):
            if leg is not None:
                leg.attachExtremity(self.centerpart.attach, i)

    def addInverseComponentAndGUI(self, targetMechaLink,
                                  positionWeight=1.,
                                  orientationWeight=0.,
                                  withGUI=True,
                                  barycentric=False) -> None:
        """
        Adds the inverse components to the Emio robot.
        The components are used to control the robot's movements.
        Two components `PositionEffector` are added to the effector node of Emio. One to control the position and one to control the orientation.
        Also adds the GUI elements of the graphical user interface for SOFA robotics. 
        It uses a user-friendly interface to control the Emio robot's parameters and visualize its state.
        The GUI includes windows for robot settings, movement controls, and plotting.
        We do this in the same method because the GUI needs the inverse components to be created before.

        Method Parameters:
            - `targetMechaLink`: The mechanical link to the target.
            - `positionWeight`: The weight of the position component (`PositionEffector`). Default is 1.
            - `orientationWeight`: The weight of the orientation component (`PositionEffector`). Default is 0.
            - `withGUI`: If True, add the GUI components. Default is True.
            - `barycentric`: If True, use barycentric coordinates for the effector. Default is False.
        """
        if not self._validState:
            Sofa.msg_error(self.getName(), "Emio has not been correctly initialized, cannot add the "
                                           "inverse components.")
            return

        for i, motor in enumerate(self.motors):
            motor.addObject('JointActuator', maxAngleVariation=pi / 20, 
                            maxAngle=pi if self.legs[i] is not None else 0, 
                            minAngle=-pi if self.legs[i] is not None else 0
                            )

        if positionWeight > 0.:
            self.effector.addObject('PositionEffector' if not barycentric else "BarycentricCenterEffector",
                                    template='Rigid3', indices=[0],
                                    useDirections=[1, 1, 1, 0, 0, 0],
                                    weight=positionWeight,
                                    maxSpeed=1000,
                                    limitShiftToTarget=True,
                                    maxShiftToTarget=20,  # mm
                                    effectorGoal=targetMechaLink, name="EffectorCoord")
        if orientationWeight > 0.:
            self.effector.addObject('PositionEffector' if not barycentric else "BarycentricCenterEffector",
                                    template='Rigid3', indices=[0],
                                    useDirections=[0, 0, 0, 1, 1, 1],
                                    weight=orientationWeight,
                                    effectorGoal=targetMechaLink, name="EffectorOrientation")

        if self._centerPartClass == Gripper:
            self.centerpart.addGripperEffector()

        if withGUI:
            self.addObject(EmioGUI(self))

        return

    def addConnectionComponents(self) -> None:
        """
        Adds the connection components to the Emio robot.
        The components are used to connect the simulation to the real robot.
        """
        from parts.controllers.motorcontroller import MotorController

        actuators = []
        for motor in self.motors:
            if motor is not None and motor.getObject("JointActuator") is not None:
                if motor.JointActuator.findData("angle"):
                    actuators.append(motor.JointActuator.angle)
                elif motor.JointActuator.findData("displacement"):
                    actuators.append(motor.JointActuator.displacement)
            else:
                actuators.append(None)

        self.getRoot().addObject(MotorController(actuators, name="MotorController"))

    def isValid(self) -> bool:
        """
        Check if Emio is in a valid state. Returns True if Emio is in a valid state, False otherwise.
        """
        return self._validState


def getParserArgs():
    """
    Parse the command line arguments for the simulation of Emio.
    The arguments include the names and models of the legs, the position of the legs on the motor,
    the name and type of the center part, and the configuration of Emio (extended or compact).
    The arguments can be passed in any order and are optional.
    If no arguments are passed, default values are used.
    The default values are:
        - legsName: "blueleg"
        - legsModel: "beam"
        - legsPositionOnMotor: "clockwisedown counterclockwisedown clockwisedown counterclockwisedown"
        - centerPartName: "yellowpart"
        - centerPartType: "rigid"
        - configuration: "extended"
    The function returns the parsed arguments.
    If the arguments are invalid, an error message is displayed and default values are used.

    For more information on the arguments, see the help message:
    ```bash
    runSofa -l SofaPython3,SofaImGui emio.py --argv --help
    ```
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Simulate the robot Emio.')
    parser.add_argument('-ln', '--legsName', type=str, nargs='*',
                        help="name of the leg (ex: blueleg, greenleg, greyleg)",
                        default='blueleg', dest="legsName")
    parser.add_argument('-lm', '--legsModel', type=str, nargs='*',
                        help="name of the model (beam, cosserat, or tetra)",
                        default='beam', dest="legsModel")
    parser.add_argument('-lp', '--legsPositionOnMotor', type=str, nargs='*',
                        help="position on motor (clockwiseup, counterclockwiseup, clockwisedown, or counterclockwisedown)",
                        default='clockwisedown counterclockwisedown clockwisedown counterclockwisedown', dest="legsPositionOnMotor")
    parser.add_argument('-cn', '--centerPartName', type=str, nargs='?',
                        help="name of the center part (ex: whitepart, yellowpart, bluepart)",
                        default='yellowpart', dest="centerPartName")
    parser.add_argument('-ct', '--centerPartType', type=str, nargs='?',
                        help="type of the center part (either deformable or rigid)",
                        default='rigid', dest="centerPartType")
    parser.add_argument('-c', "--configuration", type=str, nargs='?',
                        help="configuration of Emio, either extended or compact",
                        default='extended', dest="configuration")
    parser.add_argument('--no-connection', dest="connection", action='store_false',
                        help="use when you want to run the simulation without the robot")

    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    return args


def createScene(rootnode):
    from utils.header import addHeader, addSolvers
    from parts.controllers.assemblycontroller import AssemblyController
    """
    Test the simulation of Emio.

    Usage:
    runSofa emio.py
    """

    args = getParserArgs()

    settings, modelling, simulation = addHeader(rootnode, inverse=True)

    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)
    rootnode.VisualStyle.displayFlags.value = ["hideBehavior"]

    extended = (args.configuration=="extended")
    emio = Emio(name="Emio",
                legsName=getListFromArgs(args.legsName),
                legsModel=getListFromArgs(args.legsModel),
                legsPositionOnMotor=getListFromArgs(args.legsPositionOnMotor),
                centerPartName=args.centerPartName,
                centerPartType=args.centerPartType,
                extended=extended)
    if not emio.isValid():
        return

    simulation.addChild(emio)
    emio.attachCenterPartToLegs()
    emio.addObject(AssemblyController(emio))

    # Add effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1])
    emio.effector.addObject("RigidMapping", index=0)

    effectorTarget = modelling.addChild('Target')
    effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    effectorTarget.addObject('MechanicalObject', template='Rigid3',
                             position=[0, -130, 0, 0, 0, 0, 1] if extended else [0, 130, 0, 0, 0, 0, 1],
                             showObject=True, showObjectScale=20)
    emio.addInverseComponentAndGUI(effectorTarget.getMechanicalState().position.linkpath)

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()

    return rootnode
