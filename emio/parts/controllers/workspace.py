import Sofa
from splib3.numerics import Vec3
import numpy as np


class WorkspaceExplorer(Sofa.Core.Controller):
    """
    Explore the workspace of the robot.
    If height is given, it will only explore the corresponding plane.
    """

    def __init__(self, root, effector, assemblyController, height=None):
        Sofa.Core.Controller.__init__(self)
        self.name = "WorkspaceExplorer"
        self.height = height

        self.target = root.Modelling.Target.getMechanicalState()
        self.effector = effector
        self.assemblyController = assemblyController

        # TODO This is missing, needs to be added to the binaires
        self.markers = root.Modelling.addObject("DisplayPointsError",
                                                name="Markers",
                                                drawScale=2,
                                                exportPosition1=False,
                                                filename="Emio_outofworkspace")

        self.step = 2  # mm
        self.bound = 70
        self.initPosition = np.copy(self.target.position.value[0])
        self.target.position.value = [[-self.bound + self.initPosition[0],
                                       -self.bound + self.initPosition[1] if height is None else height,
                                       -self.bound + self.initPosition[2],
                                       0, 0, 0, 1]]
        self.dirX = 1
        self.dirZ = 1

        self.done = False

    def onAnimateBeginEvent(self, e):

        if self.assemblyController.done and not self.done:

            with self.target.position.writeable() as position:

                position[0][0] += self.step * self.dirX

                if position[0][0] > self.bound + self.initPosition[0] or position[0][0] < -self.bound + self.initPosition[0]:
                    self.dirX *= -1
                    position[0][2] += self.step * self.dirZ

                if position[0][2] > self.bound + self.initPosition[2] or position[0][2] < -self.bound + self.initPosition[2]:
                    self.dirZ *= -1
                    position[0][2] += self.step * self.dirZ

                    if self.height is None:
                        position[0][1] += self.step
                    else:
                        self.done = True

                if position[0][1] > self.bound + self.initPosition[1]:
                    self.done = True

    def onAnimateEndEvent(self, e):

        delta = Vec3(self.effector.delta.value).getNorm()
        if self.assemblyController.done and not self.done:
            if delta > 5:  # mm
                target = [self.target.position.value[0][i] for i in range(3)]
                self.markers.position1.value = list(self.markers.position1.value) + [target]
                self.markers.position2.value = list(self.markers.position2.value) + [target]
