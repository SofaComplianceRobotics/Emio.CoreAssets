import emio.parameters

import Sofa
Sofa.msg_deprecated("parameters", "Importing from the parameters module is now deprecated. You have until v26.12 to update your code. Use emio.parameters instead.")

import sys
sys.modules["parameters"] = emio.parameters