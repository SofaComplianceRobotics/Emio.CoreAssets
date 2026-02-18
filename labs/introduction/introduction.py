import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../")


def createScene(rootnode):
    from emio.utils.header import addHeader, addSolvers
    from emio.utils import getListFromArgs
    from emio.parts.controllers.assemblycontroller import AssemblyController
    from emio.parts.emio import Emio, getParserArgs

    args = getParserArgs()

    settings, modelling, simulation = addHeader(rootnode, inverse=True)

    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)

    # Add Emio to the scene
    # The args are set from introduction.md 
    emio = Emio(name="Emio",
                legsName=getListFromArgs(args.legsName),
                legsModel=getListFromArgs(args.legsModel),
                legsPositionOnMotor=getListFromArgs(args.legsPositionOnMotor),
                centerPartName=args.centerPartName,
                centerPartType=args.centerPartType,
                extended=True)
    if not emio.isValid():
        return

    simulation.addChild(emio)
    emio.attachCenterPartToLegs()
    emio.addObject(AssemblyController(emio))

    # Effector
    emio.effector.addObject("MechanicalObject", template="Rigid3", position=[0, 0, 0, 0, 0, 0, 1])
    emio.effector.addObject("RigidMapping", index=0)

    # Target
    effectorTarget = modelling.addChild('Target')
    effectorTarget.addObject('EulerImplicitSolver', firstOrder=True)
    effectorTarget.addObject('CGLinearSolver', iterations=50, tolerance=1e-10, threshold=1e-10)
    effectorTarget.addObject('MechanicalObject', template='Rigid3',
                             position=[0, -150, 0, 0, 0, 0, 1],
                             showObject=True, showObjectScale=20)

    # Inverse components and GUI
    emio.addInverseComponentAndGUI(effectorTarget.getMechanicalState().position.linkpath)

    # Components for the connection to the real robot 
    if args.connection:
        emio.addConnectionComponents()

    return rootnode
