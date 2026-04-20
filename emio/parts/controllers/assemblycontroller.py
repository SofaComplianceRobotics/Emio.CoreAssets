import Sofa
from Sofa import SofaConstraintSolver  # This is needed for the ConstraintSolver binding to work


# Animate the assembly of the robot
class AssemblyController(Sofa.Core.Controller):

    def __init__(self, emio):
        Sofa.Core.Controller.__init__(self)
        self.name = "AssemblyController"

        self.root = emio.getRoot()
        self.emio = emio
        self.legs = emio.legs
        self.motors = emio.motors

        self.dt = self.root.dt.value
        self.duration = 1.
        self.time = 0.
        self.done = False

    def onSolveConstraintSystemEndEvent(self, e):
        if not self.done:
            forces = self.root.ConstraintSolver.lambda_force()  # pointer on lambda
            for motor in self.motors:
                if motor.getObject("JointActuator") is not None:
                    # Overwrite SOFA results
                    forces[motor.JointActuator.constraintIndex.value] = 0.

    def onAnimateBeginEvent(self, e):

        if not self.done:

            self.time += self.dt

            if self.time >= self.duration:
                self.done = True
            else:
                coef = 2 ** ((self.time / self.duration) * 25 - 25)
                stiffness = coef * 1e7
                angularStiffness = coef * 1e14

                for leg in self.legs:
                    if leg is not None and leg.attachSpring is not None:
                        leg.attachSpring.stiffness.value = [stiffness]
                        leg.attachSpring.angularStiffness.value = [angularStiffness]
