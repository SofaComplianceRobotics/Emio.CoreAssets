import Sofa
import numpy
import numpy as np
from math import pi, cos
from scipy import signal
from operator import itemgetter
from splib3.numerics import Quat, Vec3, vadd, vsub

from emioapi import EmioAPI
from emioapi.emiocamera import EmioCamera, CalibrationStatusEnum

import Sofa.ImGui as MyGui
import emio.parameters as params

CLIP_DIST = np.array([0.4, 0.1, 0.4])


class DotTracker(Sofa.Core.Controller):

    def __init__(self, root, 
                 configuration="extended", # configuration of Emio, either "compact" or "extended"
                 nb_tracker=4,
                 show_video_feed=False,
                 compute_point_cloud=False,
                 track_colors=True,
                 scale=1,
                 filter_alpha=0.5,
                 *args, **kwargs):
        

        # These are needed (and the normal way to override from a python class)
        Sofa.Core.Controller.__init__(self, *args, **kwargs)
        self.root = root
        self.nb_tracker = nb_tracker
        self.compute_point_cloud = compute_point_cloud
        self.track_colors = track_colors

        # Filter
        self.filter_alpha = filter_alpha
        self.trackersf1 = np.zeros((nb_tracker,3))
        self.trackersf2 = np.zeros((nb_tracker,3))

        self.tracker = EmioCamera(show=show_video_feed, 
                                  track_markers=track_colors,
                                  compute_point_cloud=self.compute_point_cloud,
                                  configuration=configuration
                                  )
        
        self.node = root.addChild("DepthCamera")

        if self.track_colors:
            coord_pt = [0.0, 0, 0] * nb_tracker

            self.mo = self.node.addObject("MechanicalObject", name="Trackers", template="Vec3d",
                                            position=coord_pt.copy(), showObject=True,
                                            showObjectScale=7, drawMode=1, showColor=[0, 1., 0, 1])

        if self.compute_point_cloud:
            coord_pt = np.clip(self.tracker.point_cloud, -CLIP_DIST, CLIP_DIST)

            self.mo_point_cloud = self.node.addObject("MechanicalObject", name="pointCloud", template="Vec3d",
                                                        position=coord_pt, showObject=True, showObjectScale=1,
                                                        showColor=[0, 255, 0, 0.1], scale=scale*1e3)


    def onAnimateBeginEvent(self, _):
        if not self.tracker.is_running:
            if self.root.MotorController.emiomotors.is_connected:
                index = self.root.MotorController.emiomotors.device_index
                if index is not None:
                    self.tracker.open(EmioAPI.listCameraDevices()[index])
            else:
                return

        # Called at each begin of animation step
        alpha = self.filter_alpha
        if self.track_colors:
            self.tracker.update()
            coord = self.tracker.trackers_pos

            if len(coord) >= self.nb_tracker:
                # Filter
                arr = np.empty((self.nb_tracker, 3))
                arr[:] = coord[:self.nb_tracker]
                self.trackersf1 = alpha*self.trackersf1 + (1.-alpha)*arr
                self.trackersf2 = alpha*self.trackersf2 + (1.-alpha)*np.array(self.trackersf1)
                self.mo.position.value = self.trackersf2.copy()
                self.mo.reinit()

        if self.compute_point_cloud:
            coord_pt = np.clip(self.tracker.point_cloud, -CLIP_DIST, CLIP_DIST)

            self.mo_point_cloud.position.value = coord_pt.copy()
            self.mo_point_cloud.reinit()
