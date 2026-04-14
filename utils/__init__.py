import emio.utils

import Sofa
Sofa.msg_deprecated("utils", "Importing from the utils package is now deprecated. You have until v26.12 to update your code. Use emio.utils instead.")

import sys
sys.modules["utils"] = emio.utils