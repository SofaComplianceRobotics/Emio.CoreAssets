"""
This module defines the Camera class, which represents the Emio camera positioned as it would be on the real device. 

The `camera.py` file also includes an example usage. You can test it by running the script with the `runSofa` command:
```bash
runSofa -l SofaPython3,SofaImGui -g imgui camera.py
```
"""

import Sofa
from splib3.loaders import getLoadingLocation


class Camera(Sofa.Prefab):
    """
    Represents the Emio camera in the simulation.

    This class adds the camera to the simulation. The camera can be configured 
    in two modes:
    
    - compact: The camera is oriented upwards.
    - extended: The camera is oriented downwards.

    By default, the camera is added to the Emio class.

    Class Variables:
        - `extended` (`bool`): Specifies the configuration of the camera. `True` for extended mode, `False` for compact mode.

    Example Usage:
    ```python
    from emio.parts.camera import Camera

    def createScene(root):
        camera = root.addChild(Camera(extended=True))
    ```
    """
    prefabParameters = [
        {'name': 'extended', 'type': 'bool', 'help': 'configuration of Emio, true for extended, false for compact', 'default': True},
    ]

    def __init__(self, *args, **kwargs):
        Sofa.Prefab.__init__(self, *args, **kwargs)

        self.support = None

        self.addObject('RequiredPlugin', pluginName=['Sofa.Component.IO.Mesh' # Needed to use components [MeshSTLLoader]  
                                                     ,'Sofa.GL.Component.Rendering3D']) # Needed to use components [OglModel] 

        self.addObject("MeshSTLLoader",
                       filename=getLoadingLocation("../../data/meshes/camera.stl", __file__),
                       translation=[-103.94, 5, -103.94],
                       rotation=[45, 45, 0] if self.extended.value else [-45, 45, 0]) 
        self.addObject("OglModel", src=self.MeshSTLLoader.linkpath, 
                       color=[0.4, 0.4, 0.4, 1.])


def createScene(rootnode):

    rootnode.addObject("DefaultAnimationLoop")
    rootnode.addChild(Camera())

    box = rootnode.addChild("Box")
    box.addObject("MeshSTLLoader", filename=getLoadingLocation("../../data/meshes/base-compact.stl", __file__))
    box.addObject("OglModel", src=box.MeshSTLLoader.linkpath, color=[1, 1, 1, 1])