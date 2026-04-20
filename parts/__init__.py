import emio.parts 
import emio.parts.robot

import Sofa
Sofa.msg_deprecated("parts", "Importing from the parts package is now deprecated. You have until v26.12 to update your code. Use emio.parts instead.")

import sys
sys.modules["parts"] = emio.parts
sys.modules["parts.emio"] = emio.parts.robot