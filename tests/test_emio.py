from tests import partTest
import os

def test_emio():
    partTest(os.path.dirname(os.path.abspath(__file__)) + "/../emio/parts/emio.py", "--no-connection", 40)

