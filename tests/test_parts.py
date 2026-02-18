from tests import partTest
import os


def test_leg():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/leg.py")
    for leg in ["blueleg", "whiteleg"]:
        for model in ["cosserat", "beam", "tetra"]:
            partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/leg.py", "-n," + leg + ",-m," + model)


def test_centerpart():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/centerpart.py")


def test_emio():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/emio.py", "--no-connection")
    for leg in ["blueleg", "whiteleg"]:
        for model in ["beam", "tetra"]:
            partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/emio.py", "-ln," + leg + ",-lm," + model + ",--no-connection")


def test_motor():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/motor.py")


def test_camera():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/camera.py")

