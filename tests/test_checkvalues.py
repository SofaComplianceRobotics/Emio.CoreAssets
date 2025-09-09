import os
import sys
import Sofa.Simulation
import numpy as np
import pytest
from math import pi

sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../labs/lab_models/") # to import myparameters.py
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../labs/lab_inversekinematics/") # to import myQP_lab_inversekinematics.py

from labs.lab_models.lab_models import createScene as createLabModelsScene
from labs.lab_inversekinematics.lab_inversekinematics import createScene as createLabInverseKinematicsScene


# Needs SOFA_ROOT to be set to the build directory of SOFA

def getPositionCopyTestedNonEmpty(mechanicalstate):
    positions = mechanicalstate.position.value
    assert len(positions) > 0
    return np.copy(positions)

## TESTS LAB MODELS
def run_simulation_and_test_position(node):
    createLabModelsScene(node)
    nbTimeStep = 20

    Sofa.Simulation.init(node)
    extremity = node.Simulation.Leg.LegRigidExtremity.getMechanicalState()

    p0 = getPositionCopyTestedNonEmpty(extremity)[0]

    # Test that the leg do not move after nbTimeStep of simulation
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(extremity)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(p1[0], abs=5), "check the leg's extremity position"
    assert p0[1] == pytest.approx(p1[1], abs=5), "check the leg's extremity position"
    assert p0[2] == pytest.approx(p1[2], abs=5), "check the leg's extremity position"

    # Test that the leg moves up if we apply a positive rotation of the motor after nbTimeStep of simulation
    node.Simulation.Motor.JointConstraint.value.value = pi/4.
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(extremity)[0]
    # The scene is in mm
    assert p0[1] < p1[1], "check that the leg moved upward"

    # Test that the leg moves up if we apply a negative rotation of the motor after nbTimeStep of simulation
    node.Simulation.Motor.JointConstraint.value.value = -pi/4.
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(extremity)[0]
    # The scene is in mm
    assert p0[1] < p1[1], "check that the leg moved upward"


def test_lab_models_checkValues_blueleg_beam():
    sys.argv = ["lab_models", "blueleg", "beam"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "blueleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"

def test_lab_models_checkValues_blueleg_cosserat():
    sys.argv = ["lab_models", "blueleg", "cosserat"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "blueleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"
    
def test_lab_models_checkValues_blueleg_tetra():
    sys.argv = ["lab_models", "blueleg", "tetra"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "blueleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"

def test_lab_models_checkValues_whiteleg_beam():
    sys.argv = ["lab_models","whiteleg","beam"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "whiteleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"

def test_lab_models_checkValues_whiteleg_cosserat():
    sys.argv = ["lab_models", "whiteleg", "cosserat"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "whiteleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"
    
def test_lab_models_checkValues_whiteleg_tetra():
    sys.argv = ["lab_models", "whiteleg", "tetra"]
    node = Sofa.Core.Node("root")
    run_simulation_and_test_position(node)
    assert "whiteleg" in node.Simulation.Leg.Volume.MeshSTLLoader.filename.value, "check leg's name"

## TESTS LAB INVERSE KINEMATICS
def test_inverse_kinematics_exercise1():
    nbTimeStep = 200

    # Exercise 1
    sys.argv = ['lab_inversekinematics', '--legsName', 'blueleg-direct', '--legsModel', 'beam', '--legsPositionOnMotor', 'clockwisedown', 'clockwisedown', 'clockwisedown', 'clockwisedown', '--centerPartName', 'bluepart', '--no-connection']
    node = Sofa.Core.Node("root")
    exercise1, exercise2, exercise3 = createLabInverseKinematicsScene(node)

    assert exercise1 == True
    assert exercise2 == False
    assert exercise3 == False

    Sofa.Simulation.init(node)

    # Check expected values
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    effector = node.Simulation.Emio.CenterPart.Effector.getMechanicalState()

    p0 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(0, abs=0.1), "check the effector x position"
    assert p0[1] == pytest.approx(-154.8, abs=0.1), "check the effector y position"
    assert p0[2] == pytest.approx(0, abs=0.1), "check the effector z position"

    # Check convergence
    Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(p1[0], abs=1e-6), "check the effector x position"
    assert p0[1] == pytest.approx(p1[1], abs=1e-6), "check the effector y position"
    assert p0[2] == pytest.approx(p1[2], abs=1e-6), "check the effector z position"

def test_inverse_kinematics_exercise2():
    nbTimeStep = 200

    sys.argv = ['lab_inversekinematics', '--legsName', 'blueleg', '--legsModel', 'beam', '--legsPositionOnMotor', 'counterclockwisedown', 'clockwisedown', 'counterclockwisedown', 'clockwisedown', '--centerPartName', 'bluepart', '--no-connection']

    node = Sofa.Core.Node("root")
    exercise1, exercise2, exercise3 = createLabInverseKinematicsScene(node)

    assert exercise1 == False
    assert exercise2 == True
    assert exercise3 == False

    Sofa.Simulation.init(node)

    # Check expected values
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    effector = node.Simulation.Emio.CenterPart.Effector.getMechanicalState()

    p0 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(0, abs=0.1), "check the effector x position"
    assert p0[1] == pytest.approx(-154.8, abs=0.1), "check the effector y position"
    assert p0[2] == pytest.approx(0, abs=0.1), "check the effector z position"

    # Check convergence
    Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(p1[0], abs=1e-6), "check the effector x position"
    assert p0[1] == pytest.approx(p1[1], abs=1e-6), "check the effector y position"
    assert p0[2] == pytest.approx(p1[2], abs=1e-6), "check the effector z position"

def test_inverse_kinematics_exercise3():
    nbTimeStep = 200

    sys.argv = ['lab_inversekinematics', '--legsName', 'whiteleg', '--legsModel', 'beam', '--legsPositionOnMotor', 'counterclockwisedown', 'clockwisedown', 'counterclockwisedown', 'clockwisedown', '--centerPartName', 'bluepart', '--no-connection']

    node = Sofa.Core.Node("root")
    exercise1, exercise2, exercise3 = createLabInverseKinematicsScene(node)

    assert exercise1 == False
    assert exercise2 == False
    assert exercise3 == True

    Sofa.Simulation.init(node)

    # Check expected values
    for i in range(nbTimeStep):
        Sofa.Simulation.animate(node, 0.01)

    effector = node.Simulation.Emio.CenterPart.Effector.getMechanicalState()

    p0 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(0, abs=0.1), "check the effector x position"
    assert p0[1] == pytest.approx(-130.1, abs=0.1), "check the effector y position"
    assert p0[2] == pytest.approx(0, abs=0.1), "check the effector z position"

    # Check convergence
    Sofa.Simulation.animate(node, 0.01)

    p1 = getPositionCopyTestedNonEmpty(effector)[0]
    # The scene is in mm
    assert p0[0] == pytest.approx(p1[0], abs=1e-6), "check the effector x position"
    assert p0[1] == pytest.approx(p1[1], abs=1e-6), "check the effector y position"
    assert p0[2] == pytest.approx(p1[2], abs=1e-6), "check the effector z position"
