
import os
import subprocess


def test_imguibindings():
    filename = os.path.dirname(os.path.abspath(__file__)) + "/../labs/introduction/introduction.py"
    argv = "--no-connection"

    if os.path.isfile(filename):
        stderr = ""
        args = ["runSofa", filename, "-l", "SofaPython3,SofaImGui", "-g", "imgui"]
        if argv is not None:
            args += ["--argv", argv]
        try:
            subprocess.run(args, capture_output=True, timeout=10, text=True, encoding="utf-8")
        except subprocess.TimeoutExpired as e:
            assert "Finished validating" in str(e.stdout)
            for output in [e.stdout, e.stderr]:
                assert "[ERROR]" not in str(output)
                assert "segfault" not in str(output)
    else:
        raise FileNotFoundError(filename)
