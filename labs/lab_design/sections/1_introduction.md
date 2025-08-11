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
