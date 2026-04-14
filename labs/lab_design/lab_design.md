# Lab Design 

## Design of the Legs and the Gripper of Emio

::: highlight
##### Overview

In this lab session, we will work on the design of the flexible legs composing Emio such that a pick & place task can be realized.
In particular, we aim at picking an object which is not reachable with the initial design of the robot.
For that purpose, we propose you to follow an iterative and interactive design process where fast mechanical simulations are used 
to predict the system behavior and performances.
:::

:::highlight
#icon("warning") **Warning:**
This lab does NOT work on macOS due to an issue with the `gmsh` python module.
:::

:::: highlight 
#icon("info") **Important:**

![](assets/data/images/freecad-logo.png){width=19% align=right style="margin:50px 50px 20px 50px"}

We use FreeCAD and Gmsh to design the legs and generate the meshes needed for simulation. 
Depending on your operating system and your FreeCAD installation, Gmsh may or may not be included in the FreeCAD installation binaries.
Click on the following button and try the command `import gmsh` in the python console of FreeCAD (**View**>**Panels**>**Python Console**). If something does not work follow the instructions below, otherwise you can start following the lab and enjoy!

#open-button(file="assets/labs/lab_design/data/meshes/legs/my-leg-cad.FCStd")

::: collapse Troubleshooting
1. We encourage you to install [FreeCAD](https://www.freecad.org/downloads.php?) 1.0.1 or newer. 
2. Add FreeCAD executable to your environment variable Path and set FreeCAD as the default application for files with extension `.FCStd`. This will allow the open buttons of this lab to launch FreeCAD.  
3. Run the command `import gmsh` in the python console of FreeCAD (**View**>**Panels**>**Python Console**). If no import error shows, it confirms that the module is correctly installed and you can move on with the lab.
4. If Gmsh is not integrated:
   1. If you used snap to install freecad, open a terminal and install Gmsh module by running: 
        ```console
        freecad.pip install gmsh
        ```  
   2. For other installation methods. Locate the python executable of FreeCAD. In the python console of FreeCAD:
        ```python
        from freecad.utils import get_python_exe; get_python_exe()
        ```
      Now open a terminal, and install Gmsh module for the python executable of FreeCAD: 
        ```console 
        PATH_TO_FREECAD_PYTHON/python -m pip install gmsh
        ```
      **On Windows**, if the path contains spaces you will have to put it in quotation marks `"PATH_TO_FREECAD_PYTHON/python.exe"`. When using PowerShell, add an extra `&` at the beginning of the command:
        ```console
        & "PATH_TO_FREECAD_PYTHON/python.exe" -m pip install gmsh
        ```
    3. Restart FreeCAD and run the command `import gmsh` in the python console of FreeCAD to check that the module is correctly installed.  
      
:::
::::

:::: highlight 
#icon("info") **3D Printing of Flexible Parts:**

![](assets/data/images/accessories.jpg){width=19% align=right style="margin:25px"}

Emio's legs (and gripper) were printed using TPU [filament](https://shop3d.ca/collections/flexible-filaments-tpu/products/bambu-lab-tpu-hf-1-75mm-1kg) with a Bambu Lab A1. Deactivate the AMS option on the Bambu Lab. For the infill, we recommend a 100% concentric pattern. You'll also get better results if you use a 0.6mm nozzle.
::::

#include(assets/labs/lab_design/sections/1_introduction.md)
#include(assets/labs/lab_design/sections/2_determination.md)
#include(assets/labs/lab_design/sections/3_generation.md)
#include(assets/labs/lab_design/sections/4_iterations.md)
#include(assets/labs/lab_design/sections/5_deformablegripper.md)

::: highlight
#icon("user-circle") **Authors: [Quentin Peyron](https://www.linkedin.com/in/quentin-peyron-22924683/?originalSubdomain=fr) & Compliance Robotics**

![](assets/data/images/authors/quentinpeyron.png){width="15%" align="right" style="margin:25px"}

Quentin Peyron is currently a Researcher with INRIA, DEFROST Team, Lille, France. His research interests include the modeling, singularity analysis, design and control of deformable robots. He focuses in particular on the eco-design of soft parallel robots, which are promising candidates to tackle social and environmental challenges in robotics.
:::
