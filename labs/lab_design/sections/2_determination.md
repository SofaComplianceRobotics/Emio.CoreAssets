::::: collapse Determination of the Design Specifications
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

:::: quiz 
**Question:**
::: question While the four first elements of the design specifications are explained or understandable, the 5th one requires more attention as it might hide additional constraints in the design. What kind of constraints are brought by additive manufacturing, and in particular the Fused Filament Deposit principle ?
Additive manufacturing, particularly the Fused Filament Deposition (FFD) method, introduces several constraints. 
First, there is a limitation on the minimum thickness of parts, which is determined by the nozzle diameter and the layer thickness. 
Additionally, there is a maximum size constraint; the parts must fit within the printer's build volume.
Another important constraint is that the mechanical properties of the printed parts are anisotropic, meaning they vary based on the print orientation. 
For slender parts that need to bend, it is preferable to orient them so that their planes are parallel to the print bed, as this provides better flexural strength.
:::
::::

:::::