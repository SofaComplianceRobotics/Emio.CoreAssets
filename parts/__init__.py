import emio.parts 
import emio.parts.robot

import Sofa
Sofa.msg_deprecated("parts", "Importing from the parts package is now deprecated. Use emio.parts instead.")

import sys
sys.modules["parts"] = emio.parts
sys.modules["parts.emio"] = emio.parts.robot