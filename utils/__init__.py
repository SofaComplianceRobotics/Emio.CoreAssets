import emio.utils

import Sofa
Sofa.msg_deprecated("utils", "Importing from the utils package is now deprecated. Use emio.utils instead.")

import sys
sys.modules["utils"] = emio.utils