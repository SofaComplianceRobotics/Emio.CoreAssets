import os
import os.path
import emio.parameters as parameters
import Sofa

def getParserArgs():
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
    parser.add_argument('-lmd', '--legsMassDensity', type=str, nargs='*',
                        help="list of mass density of each leg",
                        default='1.220e-6', dest="legsMassDensity")
    parser.add_argument('-lpr', '--legsPoissonRatio', type=str, nargs='*',
                        help="list of Poisson ratio of each leg",
                        default='0.45', dest="legsPoissonRatio")
    parser.add_argument('-lym', '--legsYoungModulus', type=str, nargs='*',
                        help="list of Young modulus of each leg",
                        default='3.5e4', dest="legsYoungModulus")
    parser.add_argument('-cn', '--centerPartName', type=str, nargs='?',
                        help="name of the center part (ex: whitepart, yellowpart, bluepart)",
                        default='yellowpart', dest="centerPartName")
    parser.add_argument('-ct', '--centerPartType', type=str, nargs='?',
                        help="type of the center part (either deformable or rigid)",
                        default='rigid', dest="centerPartType")
    parser.add_argument('-cm', '--centerPartModel', type=str, nargs='?',
                        help="if deformable, model of the center part (either beam, cosserat or tetra)",
                        default='beam', dest="centerPartModel")
    parser.add_argument('-cmd', '--centerPartMassDensity', type=str, nargs='?',
                        help="center part mass density",
                        default='1.220e-6', dest="centerPartMassDensity")
    parser.add_argument('-cpr', '--centerPartPoissonRatio', type=str, nargs='?',
                        help="center part Poisson ratio",
                        default='0.45', dest="centerPartPoissonRatio")
    parser.add_argument('-cym', '--centerPartYoungModulus', type=str, nargs='?',
                        help="center part Young modulus",
                        default='3.5e4', dest="centerPartYoungModulus")
    parser.add_argument('-c', "--configuration", type=str, nargs='?',
                        help="configuration of Emio, either extended or compact",
                        default='extended', dest="configuration")
    parser.add_argument('-cam', "--camera", type=str, nargs='?',
                        help="enable or disable the camera, either 'enable' or 'disable'",
                        default='disable', dest="camera")
    parser.add_argument('-camf', "--cameraFeed", type=str, nargs='?',
                        help="enable or disable the camera feed, either 'enable' or 'disable'",
                        default='disable', dest="cameraFeed")
    parser.add_argument('-camt', "--nbTrackers", type=str, nargs='?',
                        help="if the camera is enabled, how many trackers to use",
                        default="1", dest="nbTrackers")
    parser.add_argument('--no-connection', dest="connection", action='store_false',
                        help="use when you want to run the simulation without the robot")

    try:
        args = parser.parse_args()
        if vars(args)["centerPartModel"] == "tetra" and vars(args)["centerPartYoungModulus"] == "":
            vars(args)["centerPartYoungModulus"] = str(float(parser.get_default("centerPartYoungModulus")) * parameters.tetraYMFactor)
        for i in range(4):
            if  vars(args)["legsModel"][i] == "tetra" and vars(args)["legsYoungModulus"][i] == "":
                vars(args)["legsYoungModulus"][i] = str(float(parser.get_default("legsYoungModulus")) * parameters.tetraYMFactor)
        for argkey, argvalue in vars(args).items():
            if isinstance(argvalue, list):
                for i in range(len(argvalue)):
                    if len(argvalue[i]) == 0:
                        argvalue[i] = parser.get_default(argkey)
            elif isinstance(argvalue, str):
                if len(argvalue) == 0:
                    argvalue = parser.get_default(argkey)
            vars(args)[argkey]=argvalue
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    return args


def createScene(rootnode):
    from emio.utils.header import addHeader, addSolvers
    from emio.parts.gripper import Gripper
    from emio.parts.controllers.assemblycontroller import AssemblyController
    from emio.parts.emio import Emio
    from emio.parts.centerpart import CenterPart
    from emio.utils import getListFromArgs
    from emio.parts.controllers.trackercontroller import DotTracker
    
    import Sofa.ImGui as MyGui

    args = getParserArgs()

    settings, modelling, simulation = addHeader(rootnode, inverse=True)
    addSolvers(simulation)

    rootnode.dt = 0.03
    rootnode.gravity = [0., -9810., 0.]
    rootnode.VisualStyle.displayFlags.value = ["hideBehavior", "hideWireframe"]

    GRIPPER = ("whitepart"==args.centerPartName)
    DEFORMABLE = ("deformable"==args.centerPartType)

    # Add Emio to the scene
    extended = (args.configuration=="extended")
    emio = Emio(name="Emio",
                legsName=getListFromArgs(args.legsName),
                legsModel=getListFromArgs(args.legsModel),
                legsPositionOnMotor=getListFromArgs(args.legsPositionOnMotor),
                legsMassDensity=[float(s) for s in getListFromArgs(args.legsMassDensity)],
                legsPoissonRatio=[float(s) for s in getListFromArgs(args.legsPoissonRatio)],
                legsYoungModulus=[float(s) for s in getListFromArgs(args.legsYoungModulus)],
                centerPartName=args.centerPartName,
                centerPartType=args.centerPartType,
                centerPartModel=args.centerPartModel,
                centerPartMassDensity=float(args.centerPartMassDensity),
                centerPartPoissonRatio=float(args.centerPartPoissonRatio),
                centerPartYoungModulus=float(args.centerPartYoungModulus),
                centerPartClass=CenterPart if not GRIPPER or not DEFORMABLE else Gripper,
                extended=extended)
    if not emio.isValid():
        return

    simulation.addChild(emio)
    emio.attachCenterPartToLegs()
    emio.addObject(AssemblyController(emio))

    # Add effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1] * 4)
    emio.effector.addObject("RigidMapping", rigidIndexPerPoint=[0, 1, 2, 3])

    # Target
    effectorTarget = modelling.addChild('Target')
    effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    effectorTarget.addObject('MechanicalObject', template='Rigid3',
                             position=[0, -150, 0, 0, 0, 0, 1] if extended else [0, 150, 0, 0, 0, 0, 1],
                             showObject=True, showObjectScale=20)

    # Add inverse components and GUI
    emio.addInverseComponentAndGUI(effectorTarget.getMechanicalState().position.linkpath, barycentric=DEFORMABLE)
    MyGui.MoveWindow.setTCPLimits(-100, 100,
                                emio.motors[0].JointActuator.minAngle.value,
                                emio.motors[0].JointActuator.maxAngle.value)

    if DEFORMABLE:
        TCP = modelling.addChild("TCP")
        TCP.addObject("MechanicalObject", template="Rigid3", position=emio.effector.EffectorCoord.barycenter.linkpath)
        MyGui.setIPController(rootnode.Modelling.Target, TCP, rootnode.ConstraintSolver)

    if GRIPPER and DEFORMABLE:
        # GUI slider for the gripper opening
        MyGui.MoveWindow.addAccessory("Gripper's opening (mm)", emio.centerpart.effector.Distance.DistanceMapping.restLengths, 8, 70)
        MyGui.ProgramWindow.addGripper(emio.centerpart.effector.Distance.DistanceMapping.restLengths, 8, 70)
        MyGui.IOWindow.addSubscribableData("/Gripper", emio.centerpart.effector.Distance.DistanceMapping.restLengths)
    MyGui.ProgramWindow.importProgram(os.path.dirname(__file__)+"/mypickandplace.crprog")

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()
        
        # Add RealSense camera tracker
        if args.camera == "enable":
            try:
                rootnode.addObject(DotTracker(name="DotTracker",
                                             root=rootnode,
                                             configuration=args.configuration,
                                             nb_tracker=int(args.nbTrackers),
                                             show_video_feed=(args.cameraFeed == "enable"),
                                             track_colors=True,
                                             comp_point_cloud=False,
                                             scale=1))
            except RuntimeError:
                Sofa.msg_error(__file__, "Camera not detected")


    return rootnode
