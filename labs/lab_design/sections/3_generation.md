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
