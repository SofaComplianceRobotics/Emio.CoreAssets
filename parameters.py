import emio.parameters

import Sofa
Sofa.msg_deprecated("parameters", "Importing from the parameters module is now deprecated. Use emio.parameters instead.")

import sys
sys.modules["parameters"] = emio.parameters