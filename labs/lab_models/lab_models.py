import Sofa
import Sofa.ImGui as MyGui

import sys
import argparse
from math import pi

from emio.utils.header import addHeader, addSolvers
from emio.parts.motor import Motor
from emio.parts.leg import Leg
from emio.parts.camera import Camera
from emio.parts.controllers.trackercontroller import *

from splib3.loaders import getLoadingLocation
from splib3.numerics import Vec3, vsub


class LabGUI(Sofa.Core.Controller):

    def __init__(self, leg, motor, markers, model):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUI"
        self.root = leg.getRoot()
        self.leg = leg
        self.markers = markers

        # Simulation State Tab
        MyGui.SimulationState.addData("Motor torque (N.mm)", "M0", motor.JointConstraint.force)
        MyGui.SimulationState.addData("Motor angle (rad)", "M0", motor.JointConstraint.displacement)

        # Move Tab
        MyGui.MoveWindow.setActuators([motor.JointConstraint.value], [0], "displacement")
        MyGui.MoveWindow.setActuatorsLimits(-pi, pi)

        # My Robot Tab
        group = "Error Markers (mm)"
        MyGui.MyRobotWindow.addInformationInGroup("Marker 1", markers.error1, group)
        MyGui.MyRobotWindow.addInformationInGroup("Marker 2", markers.error2, group)


        group = "Mechanical Parameters"
        MyGui.MyRobotWindow.addSettingInGroup("Leg Young modulus", leg.youngModulus, 5e3, 1e5, group)
        MyGui.MyRobotWindow.addSettingInGroup("Leg Poisson ratio", leg.poissonRatio, 0.01, 0.49, group)

        if "tetra" not in model:
            group = "Geometric Parameters (mm)"
            MyGui.MyRobotWindow.addSettingInGroup("Thickness", leg.thickness, 1, 20, group)
            MyGui.MyRobotWindow.addSettingInGroup("Width", leg.width, 1, 20, group)

        self.markersInitDone = False

    def onAnimateBeginEvent(self, e):
        if "TetrahedronFEMForceField" in self.leg.leg.forceField.getValueString():
            self.leg.leg.TetrahedronFEMForceField.reinit()
        elif "BeamHookeLawForceField" in self.leg.deformable.forceField.getValueString():
            self.leg.deformable.BeamHookeLawForceField.reinit()
        else:
            self.leg.leg.BeamInterpolation.lengthY = [self.leg.width.value]
            self.leg.leg.BeamInterpolation.lengthZ = [self.leg.thickness.value]
            self.leg.leg.BeamInterpolation.defaultYoungModulus = [self.leg.youngModulus.value]
            self.leg.leg.BeamInterpolation.defaultPoissonRatio = [self.leg.poissonRatio.value]
            self.leg.leg.BeamInterpolation.reinit()

        if self.root.getChild("DepthCamera") is not None:
            # Compute simulation to real error
            trackers = self.root.DepthCamera.Trackers.position.value
            markers = self.markers.getMechanicalState().position.value

            if len(trackers) >= 2:
                if trackers[0][0] > trackers[0][1]:
                    self.markers.error1.value = Vec3(vsub(trackers[0][0:3], markers[1][0:3])).getNorm()
                    self.markers.error2.value = Vec3(vsub(trackers[1][0:3], markers[0][0:3])).getNorm()
                else:
                    self.markers.error1.value = Vec3(vsub(trackers[0][0:3], markers[0][0:3])).getNorm()
                    self.markers.error2.value = Vec3(vsub(trackers[1][0:3], markers[1][0:3])).getNorm()


def createScene(rootnode):
    from emio.utils import RGBAColor
    import myparameters

    parser = argparse.ArgumentParser(prog=sys.argv[0],
                                     description='Simulate a leg.')
    parser.add_argument(metavar='legName', type=str, nargs='?', help="name of the leg's sketch in the FreeCAD project",
                        default='blueleg', dest="legName")
    parser.add_argument(metavar='model', type=str, nargs='?', help="name of the model",
                        choices=["cosserat", "beam", "tetra"],
                        default='beam', dest="model")
    parser.add_argument('--no-connection', dest="connection", action='store_false',
                        help="use when you want to run the simulation without the robot")

    try:
        args = parser.parse_args()
    except SystemExit:
        Sofa.msg_error(sys.argv[0], "Invalid arguments, get defaults instead.")
        args = parser.parse_args([])

    # Header of the simulation
    settings, modelling, simulation = addHeader(rootnode, withCollision=False)
    rootnode.dt = 0.01
    rootnode.gravity = [0., -9810., 0.]
    addSolvers(simulation)

    settings.addObject('RequiredPlugin', pluginName='Sofa.Component.Constraint.Projective')
    # Needed to use components [FixedProjectiveConstraint]

    translation = [0, 0, 100]

    # Leg
    leg = Leg(name="Leg",
              legName=args.legName,
              positionOnMotor="clockwisedown",
              model=args.model,
              translation=translation,
              rotation=[0, 180, 0],
              youngModulus=myparameters.youngModulus,
              poissonRatio=myparameters.poissonRatio,
              thickness=myparameters.thickness,
              width=myparameters.width,
              )
    simulation.addChild(leg)

    # Motor
    motor = Motor(name="Motor",
                  translation=translation,
                  rotation=[0, 180, 0],
                  tempvisurotation=[-90, 180, 0])
    motor.Parts.MotorVisual.activated.value = False
    simulation.addChild(motor)

    # Attach the leg to motor
    leg.attachBase(motor.Parts, 1)

    # Load
    load = simulation.addChild("Load")
    load.addObject("MechanicalObject", template="Rigid3", position=[[0, -200, 80, 0.707, -0.707, 0., 0.]])
    load.addObject("UniformMass", totalMass=0.034)
    visual = load.addChild("Visual")
    visual.addObject("MeshSTLLoader", 
                     filename=getLoadingLocation("../../data/meshes/centerparts/greymass.stl", __file__),
                     translation=[10, 0, 0],
                     rotation=[0, 90, 0])
    visual.addObject("OglModel", src=visual.MeshSTLLoader.linkpath, color=RGBAColor.grey)
    visual.addObject("RigidMapping")

    # Attach the load to the leg
    leg.attachExtremity(load, 0)

    # Camera
    modelling.addChild(Camera())

    # Base
    box = modelling.addChild("Base")
    box.addObject("MeshSTLLoader",
                  filename=getLoadingLocation("../../data/meshes/base-extended.stl", __file__))
    box.addObject("OglModel", src=box.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.1])

    # Platform
    platform = modelling.addChild("Platform")
    platform.addObject("MeshSTLLoader",
                  filename=getLoadingLocation("../../data/meshes/supports/platform.stl", __file__))
    platform.addObject("OglModel", src=platform.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.1])

    # Drums
    for i in range(3):
        drum = modelling.addChild("Drum" + str(i+1))
        drum.addObject("MeshSTLLoader",
                       filename=getLoadingLocation("../../data/meshes/legmotorattachbase.stl", __file__),
                       rotation=[0, [90, 180, -90][i], 0],
                       translation=[[-100, 0, 0],[0, 0, -100],[100, 0, 0]][i])
        drum.addObject("OglModel", src=drum.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.1])

    # Control torques
    motor.addObject("JointConstraint", index=0, value=0, 
                    minDisplacement=-pi, maxDisplacement=pi,
                    valueType="displacement")

    # Add Markers
    markers = leg.leg.addChild("Markers")
    markers.addObject("MechanicalObject",
                      position=[[-5, -191, -22.5], [-5, -100, -22.5]] if "blue" in args.legName else [[-5, -191, -22.5], [-22, -110, -22.5]],
                      translation=translation,
                      showObject=True, showObjectScale=7, drawMode=1, showColor=[1, 0, 0, 1])
    markers.addObject("BarycentricMapping" if args.model == "tetra" else "SkinningMapping")
    markers.addData(name="error1", type="float", value=0)
    markers.addData(name="error2", type="float", value=0)

    # Set up customized GUI
    rootnode.addObject(LabGUI(leg, motor, markers, args.model))

    if args.connection:
        # Add RealSense camera tracker
        try:
            from emio.parts.controllers.motorcontroller import MotorController
            rootnode.addObject(MotorController([motor.JointConstraint.displacement, None, None, None],
                                            name="MotorController"))

            tracker = DotTracker(name="DotTracker",
                                 root=rootnode,
                                 configuration="extended",
                                 nb_tracker=2,
                                 show_video_feed=False,
                                 track_colors=True,
                                 comp_point_cloud=False,
                                 scale=1)

            rootnode.addObject(tracker)        
        except RuntimeError:
            Sofa.msg_error(__file__, "Camera not detected")


    return
