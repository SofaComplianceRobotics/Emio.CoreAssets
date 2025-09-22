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

1. Open the file `MYHOME/emio-labs/assets/labs/lab_design/data/meshes/centerparts/my-gripper-cad.FCStd` with FreeCAD.  

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

#open-button("assets/data/meshes/labs/lab_design/centerparts/my-gripper-cad.FCStd")

#runsofa-button("assets/labs/lab_design/lab_design.py", "deformable")
::::
:::::
