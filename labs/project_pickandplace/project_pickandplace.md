# Project Pick & Place

::: highlight
##### Overview

In this lab, we will test a simple pick & place example using a soft gripper attached to the robot's end-effector.
This exercise aims to apply the concepts studied and reinforce your understanding of inverse models in soft robotics 
by programming a complete pick & place cycle.
:::

::: collapse Pick & Place
## Pick & Place

*Pick & place* is a common robotic manipulation task that involves picking up an object and moving it to another location. This task can be particularly challenging when adaptability is required to handle various objects without causing damage and when the environment is cluttered. Challenges which are being addressed by soft robotics. 

In this lab, we will review the inverse models of soft robots, demonstrating how these models enable the decoupling of the robot's overall motion from the specific control of the end-effector. Specifically, we will explore how to separate the robot's overall movement from the movement of its soft gripper.
:::

:::: collapse Emio Design with a Gripper
## Emio Design with a Gripper

The native design of Emio features four legs attached with a rigid connector to form a parallel architecture. Emio is equipped with four motors, allowing control over the translation of the end-effector in the x, y, and z directions, offering three degrees of freedom (DoFs). In this project, we will introduce a 4th DoF by attaching a deformable gripper composed of two fingers to the legs. The 4th DoF will control the distance between the extremities of the gripper's fingers.

::: highlight
#icon("info-circle") **Note:** In the field of rigid robotics and compliant robotics, this structure would be typically qualified as
a parallel robot with a reconfigurable platform.
:::
::::

::::: collapse Advantages of Using a Soft Manipulator for Pick & Place
## Advantages of Using a Soft Manipulator for Pick & Place

This project highlights key advantages of soft robotics, particularly mechanical adaptability and robustness in unfamiliar environments.
Through the following exercise, you will realize that, unlike rigid robots, soft robots can adapt without breaking. They can also rely 
on physical obstacles to achieve tasks:

1. A soft manipulator allows the robot to safely make contact with its environment without risking damage.
   In fact, contact is acceptable even when the program does not avoid it entirely (see images below).

| ![](assets/data/images/emio-gripper-contact4.png){width=75%} | ![](assets/data/images/emio-gripper-contact3.png){width=75%} | 
|-------------------------------------------------------------:|:-------------------------------------------------------------| 
|                                    **1. Emio safely making** | **contact with its environment**                             |

2. While soft manipulators sacrifice some control precision, we can use contact with obstacles to achieve successful grasping and placement (see images below).

| ![](assets/data/images/emio-gripper-contact7.png){width=75%} | ![](assets/data/images/emio-gripper-contact8.png){width=75%} | 
|-------------------------------------------------------------:|:-------------------------------------------------------------| 
|                               **2. Emio using contact with** | **obstacles to achieve placement**                           |


:::: exercise 

::: collapse {open} Set up Emio
- Raise the platform using the blue elevators
- Place the blue tray on the platform using the small pins
- Put the white cube into one the the tray's slots
- Take four <span style="color:blue">*blue legs*</span> and attach them to each motor (as shown on the left image).
- Attach the *white connector* (the soft gripper) at the tip of each leg. Pay close attention to the robot's motor numbering to correctly position the gripper. **The gripper's jaws must align with motors n°0 and n°2 (as shown on the right image)**.

You should have Emio set up as shown in the left image.

![](assets/data/images/project1-emio.png){width=49%}
![](assets/data/images/project1-gripper.png){width=49%}
:::

**Exercise:**

Your task is to program Emio to perform a pick & place operation on a small cube. 
The goal is to apply the principles of inverse kinematics in soft robotics and successfully control the robot's end-effector, 
including the soft gripper's 4th DoF. This will involve picking up the cube from one location and placing it in another.

#runsofa-button("assets/labs/project_pickandplace/project_pickandplace.py")

::::
:::::



