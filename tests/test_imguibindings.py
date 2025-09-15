
import os
import subprocess
from sys import platform

def test_imguibindings():
    if platform != "win32":
        # This test is not supported on the CI on Windows (the driver does not support OpenGL)
        filename = os.path.dirname(os.path.abspath(__file__)) + "/../labs/introduction/introduction.py"
        if os.path.isfile(filename):
            timeoutRaised = False
            args = ["runSofa", filename, "-l", "SofaPython3,SofaImGui", "-g", "imgui", "--argv", "--no-connection"]
            try:
                subprocess.run(args, capture_output=True, timeout=10, text=True, encoding="utf-8")
            except subprocess.TimeoutExpired as e:
                timeoutRaised = True
                assert "Finished validating" in str(e.stdout)
                for output in [e.stdout, e.stderr]:
                    assert "[ERROR]" not in str(output)
                    assert "segfault" not in str(output)
            if not timeoutRaised:
                raise RuntimeError("The process runSofa did not run as expected.")
        else:
            raise FileNotFoundError(filename)
