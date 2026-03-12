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
    from itertools import product
    configsParams = {
        "legsName": ["blueleg"],
        "legsModel": [ "beam", "cosserat", "tetra"],
        "centerPartName": ["whitepart", "yellowpart", "bluepart"],
        "centerPartType": ["deformable", "rigid"],
        "centerPartModel": ["beam", "tetra"]
    }

    combinations = list(product(*configsParams.values()))
    combinations = list(filter(lambda t: (t[2]!="whitepart" and t[3]=="rigid" and t[4]=="beam") or t[2]=="whitepart", combinations)) # Removes non valid combinations

    for combination in combinations:
        partTest(os.path.dirname(os.path.abspath(__file__)) + "/../labs/sandbox/sandbox.py", 
                f"""--no-connection,-ln,{combination[0]},{combination[0]},{combination[0]},{combination[0]},-lm,{combination[1]},{combination[1]},{combination[1]},{combination[1]},-cn,{combination[2]},-ct,{combination[3]},-cm,{combination[4]}""", 
                40)
