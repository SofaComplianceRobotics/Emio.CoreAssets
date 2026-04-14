import os
import subprocess


def partTest(filename, argv=None, nbIterations=10):
    if os.path.isfile(filename):
        args = ["runSofa", filename, "-l", "SofaPython3,SofaImGui", "-g", "batch", "-n", str(nbIterations)]
        if argv is not None:
            args += ["--argv", argv]
        result = subprocess.run(args, capture_output=True, text=True)
        result.check_returncode()
        print("Args: ",result.args)
        print(result.stdout)
        assert str(nbIterations) + " iterations done" in result.stdout
        print("STDERR: ", result.stderr)
        assert "[ERROR]" not in result.stderr
        assert "[WARNING]" not in result.stdout 
    else:
        raise FileNotFoundError(filename)
