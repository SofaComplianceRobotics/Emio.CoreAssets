import os
import sys
import Sofa.Simulation
import numpy as np
import pytest
from math import pi

def create_scene(args=["leg"]):
    from emio.parts.leg import createScene

    node = Sofa.Core.Node("root")
    sys.argv = args
    leg = createScene(node)
    Sofa.Simulation.init(node)

    return leg


def test_initialization_leg():
    totalMass = 0.0157 # kg
    leg = create_scene(["leg","-n","blueleg","-m","beam"])
    assert leg.isValid() == True, "Correct initialization"
    assert leg.totalMass == pytest.approx(totalMass, abs=1e-4)

    leg = create_scene(["leg","-n","blueleg","-m","cosserat"])
    assert leg.isValid() == True, "Correct initialization"
    assert leg.totalMass == pytest.approx(totalMass, abs=1e-4)

    leg = create_scene(["leg","-n","blueleg","-m","tetra"])
    assert leg.isValid() == True, "Correct initialization"
    assert leg.totalMass == pytest.approx(totalMass, abs=1e-4)


def test_initialization_leg_parameters():
    leg = create_scene()
    assert leg.translation.value == pytest.approx([0., 0., 0.])
    assert leg.rotation.value == pytest.approx([0., 0., 0.])
    assert leg.width.value == pytest.approx(10.)
    assert leg.thickness.value == pytest.approx(5.)
    assert leg.crossSectionShape.value == "rectangular"
    assert leg.massDensity.value == pytest.approx(1.220e-6)
    assert leg.poissonRatio.value == pytest.approx(0.45)
    assert leg.youngModulus.value == pytest.approx(3.5e4)


def test_initialization_leg_position_on_motor():
    leg = create_scene(["leg","-p","clockwiseup"])
    assert leg.rotation.value == pytest.approx([0, 0, 0]), "Check position on motor"
    leg = create_scene(["leg","-p","clockwisedown"])
    assert leg.rotation.value == pytest.approx([180, 180, 0]) or leg.rotation.value == pytest.approx([0, 0, 180]), "Check position on motor"
    leg = create_scene(["leg","-p","counterclockwiseup"])
    assert leg.rotation.value == pytest.approx([0, 180, 0]) or leg.rotation.value == pytest.approx([180, 0, 180]), "Check position on motor"
    leg = create_scene(["leg","-p","counterclockwisedown"])
    assert leg.rotation.value == pytest.approx([180, 0, 0]) or leg.rotation.value == pytest.approx([0, 180, 180]), "Check position on motor"