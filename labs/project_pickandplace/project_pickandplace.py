import os
import os.path


def createScene(rootnode):
    from emio.utils.header import addHeader, addSolvers
    from emio.parts.gripper import Gripper
    from emio.parts.controllers.assemblycontroller import AssemblyController
    from emio import Emio, getParserArgs
    import Sofa
    import Sofa.ImGui as MyGui

    args = getParserArgs()

    settings, modelling, simulation = addHeader(rootnode, inverse=True)
    addSolvers(simulation)

    rootnode.dt = 0.05
    rootnode.gravity = [0., -9810., 0.]
    rootnode.VisualStyle.displayFlags.value = ["hideBehavior", "hideWireframe"]

    # Add Emio to the scene
    emio = Emio(name="Emio",
                legsName=["blueleg"],
                legsModel=["beam"],
                legsPositionOnMotor=["counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown"],
                centerPartName="whitepart",  # choose the gripper as the center part
                centerPartType="deformable",  # the gripper is deformable
                centerPartModel="beam",
                centerPartClass=Gripper,  # specify that the center part is a Gripper
                platformLevel=2,
                extended=True)
    if not emio.isValid():
        Sofa.msg_error(simulation, "Emio is not valid, could not add it to the scene graph.")
        return

    simulation.addChild(emio)
    emio.attachCenterPartToLegs()
    emio.addObject(AssemblyController(emio))

    # Tray
    tray = modelling.addChild("Tray")
    tray.addObject("MeshSTLLoader", filename=os.path.dirname(__file__)+"/../../data/meshes/tray.stl", translation=[0, 10, 0])
    tray.addObject("OglModel", src=tray.MeshSTLLoader.linkpath, color=[0.3, 0.3, 0.3, 0.2])

    # Add effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1] * 4)
    emio.effector.addObject("RigidMapping", rigidIndexPerPoint=[0, 1, 2, 3])

    # Target
    effectorTarget = modelling.addChild('Target')
    effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    effectorTarget.addObject('MechanicalObject', template='Rigid3',
                             position=[0, -150, 0, 0, 0, 0, 1],
                             showObject=True, showObjectScale=20)

    # Add inverse components and GUI
    emio.addInverseComponentAndGUI(effectorTarget.getMechanicalState().position.linkpath, barycentric=True)
    TCP = modelling.addChild("TCP")
    TCP.addObject("MechanicalObject", template="Rigid3", position=emio.effector.EffectorCoord.barycenter.linkpath)
    MyGui.setIPController(rootnode.Modelling.Target, TCP, rootnode.ConstraintSolver)

    # GUI slider for the gripper opening
    MyGui.MoveWindow.addAccessory("Gripper's opening (mm)", emio.centerpart.Effector.Distance.DistanceMapping.restLengths, 5, 70)
    MyGui.ProgramWindow.addGripper(emio.centerpart.Effector.Distance.DistanceMapping.restLengths, 5, 70)
    MyGui.ProgramWindow.importProgram(os.path.dirname(__file__)+"/mypickandplace.crprog")
    MyGui.IOWindow.addSubscribableData("/Gripper", emio.centerpart.Effector.Distance.DistanceMapping.restLengths)

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()

    return rootnode
