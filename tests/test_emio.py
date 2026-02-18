from tests import partTest
import os

def test_emio():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/robot.py", "--no-connection", 40)

