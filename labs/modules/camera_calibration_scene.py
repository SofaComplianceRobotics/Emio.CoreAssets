import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../../")

import Sofa
import sys
import argparse
from math import pi

from utils.header import addHeader, addSolvers

from splib3.loaders import getLoadingLocation
from splib3.numerics import Vec3, vsub

from parts.motor import Motor
from parts.leg import Leg
from parts.camera import Camera
from parts.controllers.trackercontroller import *
import Sofa.ImGui as MyGui


class LabGUI(Sofa.Core.Controller):

    def __init__(self, motor, markers, model):
        Sofa.Core.Controller.__init__(self)
        self.name = "LabGUI"
        self.root = markers.getRoot()
        self.markers = markers

        # My Robot Tab
        group = "Error Markers (mm)"
        MyGui.MyRobotWindow.addInformationInGroup("Marker 1", markers.error1, group)
        MyGui.MyRobotWindow.addInformationInGroup("Marker 2", markers.error2, group)

        self.markersInitDone = False

    def onAnimateBeginEvent(self, e):
        if self.root.getChild("DepthCamera") is not None: # Wait for the camera to be initialized
            if self.root.DotTracker.tracker is not None: # Wait for the tracker to be initialized
                if self.root.DotTracker.tracker._camera and self.root.DotTracker.tracker.calibration_status is not CalibrationStatusEnum.CALIBRATED: 
                    self.root.DotTracker.tracker.calibrate()

            # Compute simulation to real error
            trackers = self.root.DepthCamera.Trackers.position.value
            markers = self.markers.getMechanicalState().position.value

            if len(trackers) >= 2:
                # Compare closest pair of tracker / marker
                distance = Vec3(vsub(trackers[0][0:3], markers[0][0:3])).getNorm()
                if distance > 50:
                    self.markers.error1.value = Vec3(vsub(trackers[1][0:3], markers[0][0:3])).getNorm()
                    self.markers.error2.value = Vec3(vsub(trackers[0][0:3], markers[1][0:3])).getNorm()
                else:
                    self.markers.error1.value = Vec3(vsub(trackers[0][0:3], markers[0][0:3])).getNorm()
                    self.markers.error2.value = Vec3(vsub(trackers[1][0:3], markers[1][0:3])).getNorm()


def createScene(rootnode):
    from utils import RGBAColor

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

    settings.addObject('RequiredPlugin', name='Sofa.Component.Constraint.Projective')
    # Needed to use components [FixedProjectiveConstraint]

    translation = [0, 0, 100]

    # Motor
    motor = Motor(name="Motor",
                  translation=translation,
                  rotation=[0, 180, 0],
                  tempvisurotation=[-90, 180, 0])
    motor.Parts.MotorVisual.activated.value = False
    simulation.addChild(motor)


    # Camera
    camera = modelling.addChild(Camera())

    # Base
    box = modelling.addChild("Base")
    box.addObject("MeshSTLLoader",
                  filename=getLoadingLocation("../../data/meshes/base-extended.stl", __file__))
    box.addObject("OglModel", src=box.MeshSTLLoader.linkpath, color=[1, 1, 1, 0.1])

    # Calibration validation markers
    elevator = 70
    arucoThickness = 3
    platformY = -303
    y = platformY + elevator + arucoThickness 
    square = modelling.addChild("CalibrationSquare")
    square.addObject("MechanicalObject",
                      position=[[32, y, 32.0], [-32, y, -32.0]],
                      showObject=True, showObjectScale=7, drawMode=1, showColor=[1, 0, 0, 1])
    square.addData(name="error1", type="float", value=0)
    square.addData(name="error2", type="float", value=0)

    # Platform
    platform = modelling.addChild("Platform")
    platform.addObject("MeshSTLLoader", translation=[0, 70, 0],
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

    # Set up customized GUI
    rootnode.addObject(LabGUI(motor, square, args.model))

    if args.connection:
        # Add RealSense camera tracker
        try:
            from parts.controllers.motorcontroller import MotorController
            rootnode.addObject(MotorController([None, None, None, None],
                                            name="MotorController"))

            tracker = DotTracker(name="DotTracker",
                                root=rootnode,
                                nb_tracker=2,
                                show_video_feed=True,
                                track_colors=True,
                                comp_point_cloud=False,
                                scale=1)
            
            rootnode.addObject(tracker)        
        except RuntimeError:
            Sofa.msg_error(__file__, "Camera not detected")

    return