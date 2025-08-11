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

#open-button("assets/data/meshes/legs/leg-cad.FCStd")

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

:::: collapse Introduction
### Introduction

The legs and the gripper are oriented downward in a classical Delta robot configurations to manipulate objects on a working plate.
To perform the pick & place task, we propose then to separate the robot design into two sequential phases:
1. The design of the legs, considering a rigid gripper, to reach the position of the object to grasp.
2. The design of the gripper, now considered as deformable, to ensure the gripper closure on the object.

| ![](assets/data/images/pickandplace0.png) |    ![](assets/data/images/pickandplace1.png)     | ![](assets/data/images/pickandplace2.png) | 
|:------------------------------------:|:-------------------------------------------:|:------------------------------------:| 
|                                      |  **Emio performing a pick-and-place cycle** |                                      |

The goal of this hands-on session is to learn how to leverage parametric Computer Assisted Design (CAD) and mechanical models to optimize 
the leg and gripper designs iteratively. 
We propose in particular the use of a python script that will automatically generate a geometry and a mesh, starting from base designs and 
following simple inputs of design parameters.
The designs will be simulated to have an evaluation of the pick & place success.
According to the performances obtained, you will iterate manually on their design and repeat the process until the design specifications are achieved.

|                      ![](assets/data/images/conception-flowchart.png)                  | 
|:--------------------------------------------------------------------------------------:| 
| **Flow chart diagram of the design process, with the steps detailed in each exercise** |
::::

:::: collapse Determination of the Design Specifications
::: highlight
##### Overview

In this first part, we focus on ensuring that the leg design enables to reach the object to grasp. 
For this purpose, we will follow the steps of a classical design process. 
:::

### Determination of the Design Specifications

Any design process of a robotic system, whether it is soft or not, should be conducted to obtain desired specifications. 
The first step of the process is therefore to determine these specifications. 
They can be qualitative (ex: obtaining a bending motion with pneumatic actuation), quantitative (ex: elongating over 20% of its initial length), 
driven by an application (ex: must be soft enough not to damage living tissues in medical interventions) or 
constrained by the integration of pre-existing parts (ex: the pneumatic components supports a maximum pressure of 100kPa) or by a 
fabrication process (ex: obtained by casting). 
The larger the number of specifications, the harder the design process is, in particular when some of them are conflicting each other 
(ex: generating large forces with a soft manipulator while being compliant to have safe contacts with the environment). 
For this part of the lab session, the design specifications are as follows:
- **C1**: the object to pick is initially on the working plane at a distance of 75mm from the plate center along the X axis. 
The target location is at -75mm along the X axis as well.
- **C2**: the gripper is initially 30mm above the object to grasp.
- **C3**: the attachment position of the legs to the motor and the gripper should not change. 
This constraint has two objectives. First, it simplifies the design by reducing the amount of parameters to be varied.
Indeed, in parallel robotic design, it is classical to consider the attachments' position and orientation as design parameters. 
Second, it ensures a good regeneration of the Emio simulation scene on SOFA, and a good initial convergence of the model.
- **C4**: the legs should not collide either between them or with the robot base.
- **C5**: the leg will be produced using Fused Filament Deposit additive manufacturing. 


::: exercise
**Question:**
:::: quiz
::: question While the four first elements of the design specifications are explained or understandable, the 5th one requires more attention as it might hide additional constraints in the design. What kind of constraints are brought by additive manufacturing, and in particular the Fused Filament Deposit principle ?
Additive manufacturing, particularly the Fused Filament Deposition (FFD) method, introduces several constraints. 
First, there is a limitation on the minimum thickness of parts, which is determined by the nozzle diameter and the layer thickness. 
Additionally, there is a maximum size constraint; the parts must fit within the printer's build volume.
Another important constraint is that the mechanical properties of the printed parts are anisotropic, meaning they vary based on the print orientation. 
For slender parts that need to bend, it is preferable to orient them so that their planes are parallel to the print bed, as this provides better flexural strength.
:::
::::

::::: collapse Choice of a Leg Design and Generation of its Geometry
### Choice of a Leg Design and Generation of its Geometry

Amongst the large variety of leg shape that could be imagined we focus here on legs that are initially slender, 
and consisting of a rectangular cross-section swept along a planar curved profile. 
This provides freedom in the design while simplifying again the design space, and ensures that the leg can be easily 3D printing.
The curved profile is constructed as a B-spline, which is defined by a series of points in the plane.
Therefore, the design parameters considered here are represented in the following figures and are listed below:
- the (**x**, **y**) coordinates of the points $p_i$ defining the b-spline of the curved profile, which will modify the curvature of the leg and its length.
The first four points and the last two points must not be changed to satisfy the constraint **C2**.
- the width **w** of the leg
- the thickness **t** of the leg

|                                                           ![](assets/data/images/legDesign.png)                                                            | 
|:---------------------------------------------------------------------------------------------------------------------------------------------------------:| 
| **Left: 3D view on the base leg design on FreeCAD; Middle: sketch editor for changing the curved profile; Right: 3D mesh of the leg generated with Gmsh** |

You can specify the width and thickness values. For the B-spline points, entering directly the position coordinates
would not be ergonomic, as it could be difficult to imagine the resulting curve.
Therefore, we propose to modify these points graphically using the open-source and free software FreeCAD.
By opening the file `MYHOME/emio-labs/assets/data/meshes/legs/leg-cad.FCStd`, you will see the window shown in the figure above.
You can then double-click on the sketch `myleg` where the points composing the spline are defined and the spline depicted.
You can finally change the point position by dragging their center. 
Please, ensure that on the very bottom right of the interface, the FreeCAD control set **CAD** is selected.

The spline is initially composed of a limited number of points to limit the number of parameters to vary manually.
You can add more points on the spline by selecting first the spline, then clicking the **Insert a node** button in the sketch toolbar, 
and finally clicking on the spline where you want to place it.

Once all the design parameters are specified, the python script `MYHOME/emio-labs/assets/utils/freecadbeziercurvetomeshes.py` is used to 
generate the parametric geometry of the leg. Using the OpenCascade tool incorporated in FreeCAD, it recovers the B-spline
from the sketch `myleg`, defines a rectangular cross-section using variables **w** and **t**, to finally extrude (sweep) this 
cross-section along the planar curved profile. 

::: highlight
#icon("info-circle") **Note:** Don't hesitate to look at the code of the script `freecadbeziercurvetomeshes.py` for details.
:::

In the exercise you will generate the geometry and the meshes required to run the different leg models of Emio using the free Gmsh software.
These meshes include:
- a 1-dimensional mesh in the form of a list of 3D points for the definition of beam and Cosserat rod models.
- a 2-dimensional mesh of the leg outer surface for visualisation and rendering
- a 3-dimensional mesh of the leg composed of tetrahedron elements for the definition of the FEM model.
The mesh density is tuned using a parameter called **size factor**. The larger the size factor, the rougher the mesh is.

::: highlight
#icon("warning") **Warning:** As a result, if the leg shape varies too fast in space (meaning the curvature is too high with sign changes), a large size
factor will induce a bad discretization and errors in the scene.
:::

:::: exercise
**Exercise 1:**

1. Change the curvature of the leg. Open the file `MYHOME/emio-labs/assets/data/meshes/legs/leg-cad.FCStd` with FreeCAD. Double-click on `mylegSketch` and make your changes.  

2. Once you're done. Still in FreeCAD, open the `View/Panels/Python console`. In the console copy and paste the following commands: 
    ```python
    import sys, os
    sys.path.append(os.path.dirname(FreeCAD.ActiveDocument.FileName)+"/../../../utils/")
    from freecadbeziercurvetomeshes import *
    ```

3. Choose the design parameters of the leg:  
    - **thickness**: in mm, between 1 and 10
    - **width**: in mm, between 1 and 20
    - **size**: mesh size factor between 0.1 and 1  

   ::: highlight
   #icon("info-circle") **Note:** The parameter **size** changes the discretization of the mesh; the smaller the value, the finer the discretization. 
   The discretization is an important parameter as it influences both the accuracy and the computation time of the simulation. 
   A mesh that is too coarse will result in fast computation time but poor accuracy, while a mesh that is too fine will 
   yield good accuracy but significantly increase computation time. 
   :::
   
   Then generate the corresponding meshes by copy and paste the following code into the python console of FreeCAD:

    ```python
    freecadCurveToMeshes(thickness=YOUR_THICKNESS, width=YOUR_WIDTH, size=YOUR_SIZE)
    ```

4. Once you're done, test your design in simulation by clicking the SOFA button.

#open-button("assets/data/meshes/legs/leg-cad.FCStd")

#runsofa-button("assets/labs/lab_design/lab_design.py", "rigid")

::::
:::::

:::: collapse Iteration on the Leg Design to Meet the Specifications
### Iteration on the Leg Design to Meet the Specifications

So far, we performed only one design iteration through steps 1 to 4. 
Model-based design processes are generally iterative. 
The performances obtained for a given design are compared to the desired ones, and the design parameters are changed by the user to reduce the error (similarly to a closed-loop control scheme). 
This iteration process can be partly to fully automated using off-the-shelf numerical optimization methods such as gradient-descent. 
Note that using these tools may require additional work, such as reformulating the soft robot model and the optimization problem to obtain a mathematical form suitable for optimization (quadratic cost function to ensure convexity for example). 
Other methods like evolutionary algorithms can also be used to search the design space of parametric designs efficiently. 
Instead of optimizing a single candidate, these methods evaluate populations of candidates which evolve over generations. 
In our case, to avoid going deep on the problem formulation and to get intuition on how the design parameters affect the finger performances, we will iterate manually on the design parameters. 

::: exercise
**Exercise 2:**

Repeat the design process until the specifications are met. 
- What are the values of **w** and **t** ? 
- What is the final curved profile of the leg ? 
- How intricate is it to find the optimal design parameters manually?

Some advices: 
- Try to vary one parameter at a time (at least at the beginning), to learn its influence on the robot behavior. 
- Keep notes of what designs you already tried. 

#runsofa-button("assets/labs/lab_design/lab_design.py", "rigid")
:::
::::

::::: collapse The Deformable Gripper
### The Deformable Gripper

Now that you have seen the different steps composing the design of a deformable robot, we propose you to work on the design of Emio's gripper.
We now consider the gripper to be deformable, so that we can use the robot 4th DoF to close the gripper and grasp an object.

:::: exercise

**Exercise 3: Design of the deformable gripper**

Follow the different steps: think about the design specifications, modify the design parameters of the gripper and 
evaluate the current design with the simulator.
This last step will involve in particular to use the gripping action available.

The gripper is composed of two fingers linked together with a ring with a square cross-section. 
The legs are then rigidly attached to this ring, and will deform it upon actuation.
As a couple design parameters, we propose you to modify the ring's thickness and the fingers opening.

1. Open the file `MYHOME/emio-labs/assets/data/meshes/centerparts/gripper-cad.FCStd` with FreeCAD.  

2. Still in FreeCAD, open the `View/Panels/Python console`. In the console copy and paste the following commands: 
    ```python
    import sys, os
    sys.path.append(os.path.dirname(FreeCAD.ActiveDocument.FileName)+"/../../../utils/")
    from freecadgrippertomeshes import *
    ```

3. Choose the design parameters of the gripper:  
    - **thickness**: in mm, between 1 and 9
    - **angle**: finger's opening angle in degree
    - **size**: mesh size factor between 0.1 and 1  
   
   ::: highlight
   #icon("info-circle") **Note:** For exemple the parameters used for the original gripper are: thickness=3, angle=50, and size=0.5.
   :::

   Then, generate the corresponding meshes by copy and paste the following code into the python console of FreeCAD:

    ```python
    freecadGripperToMeshes(thickness=YOUR_THICKNESS, angle=YOUR_ANGLE, size=YOUR_SIZE)
    ```

4. Once you're done, test your design in simulation by clicking the SOFA button.

**Questions:**

- What is the optimal value of ring thickness ? 
- How does the ring's flexibility alter the robot workspace?

#open-button("assets/data/meshes/centerparts/gripper-cad.FCStd")

#runsofa-button("assets/labs/lab_design/lab_design.py", "deformable")
::::
:::::

::: highlight
#icon("user-circle") **Authors: [Quentin Peyron](https://www.linkedin.com/in/quentin-peyron-22924683/?originalSubdomain=fr) & Compliance Robotics**

![](assets/data/images/authors/quentinpeyron.png){width="15%" align="right" style="margin:25px"}

Quentin Peyron is currently a Researcher with INRIA, DEFROST Team, Lille, France. His research interests include the modeling, singularity analysis, design and control of deformable robots. He focuses in particular on the eco-design of soft parallel robots, which are promising candidates to tackle social and environmental challenges in robotics.
:::
