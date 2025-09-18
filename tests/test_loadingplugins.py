
import os
import subprocess

def checkOutput(o):
    assert "Finished validating" in str(o.stdout)
    for output in [o.stdout, o.stderr]:
        assert "[ERROR]" not in str(output)
        assert "segfault" not in str(output)

def test_loading_required_plugins():
    args = ["runSofa", "-l", "SofaPython3,SoftRobots,SoftRobots.Inverse,BeamAdapter,Cosserat", "-g", "batch"]
    try:
        p = subprocess.run(args, capture_output=True, timeout=10, text=True, encoding="utf-8")
        checkOutput(p)
    except subprocess.TimeoutExpired as e:
        checkOutput(e)
