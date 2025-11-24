from tests import partTest
import os


def test_lab_Models():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_models/lab_models.py", "--no-connection", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_models/lab_models.py", "blueleg,beam,--no-connection", 40)


def test_lab_inversekinematics():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_inversekinematics/lab_inversekinematics.py", "--no-connection,-ln,blueleg-direct", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_inversekinematics/lab_inversekinematics.py", "-ln,whiteleg,blueleg-direct,-lm,tetra,beam,-lp,clockwiseup,-cn,yellowpart,--no-connection", 40)


def test_project_pickAndplace():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/project_pickandplace/project_pickandplace.py", "--no-connection", 40)


def test_lab_design():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_design/lab_design.py", "rigid,--no-connection", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_design/lab_design.py", "deformable,--no-connection", 40)


def test_lab_closedloop():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/lab_closedloop/lab_closedloop.py", "--no-connection", 40)


def test_sandbox():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/sandbox/sandbox.py", "--no-connection", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/sandbox/sandbox.py", "--no-connection,-cn,whitepart,-ct,deformable,-cm,tetra", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/sandbox/sandbox.py", "--no-connection,-cn,whitepart,-ct,deformable,-cm,beam", 40)
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/sandbox/sandbox.py", "--no-connection,-cn,whitepart,-ct,rigid", 40)


