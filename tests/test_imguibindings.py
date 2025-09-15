
import os
import subprocess
from sys import platform

def checkOutput(o):
    assert "Finished validating" in str(o.stdout)
    for output in [o.stdout, o.stderr]:
        assert "[ERROR]" not in str(output)
        assert "segfault" not in str(output)

def test_imguibindings():
    if platform != "win32":
        # This test is not supported on the CI on Windows (the driver does not support OpenGL)
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../labs/introduction/introduction.py"
        if os.path.isfile(filename):
            args = ["runSofa", filename, "-l", "SofaPython3,SofaImGui", "-g", "imgui", "--argv", "--no-connection"]
            try:
                p = subprocess.run(args, capture_output=True, timeout=10, text=True, encoding="utf-8")
                checkOutput(p)
            except subprocess.TimeoutExpired as e:
                checkOutput(e)
        else:
            raise FileNotFoundError(filename)
