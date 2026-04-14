::::::: collapse Kinematics of Emio
## Kinematics of Emio

In this section, we will explore the kinematic model of Emio, depending on the configurations of the legs.
After modeling each leg of the robot and the mechanical coupling between these legs (depending on the effector connector), 
we obtained the static calculations of the robot.
To observe the kinematics, you will test different configurations of Emio. 

As explained above, the kinematics of the robot can be expressed as a function that gives the position of the end-effector 
$\textcolor{darkgreen}{\mathbf{y}_{e}}$ based on the commanded motor position $\textcolor{red}{\mathbf{u}_{a}}$. 
To compute this function, we will modify the static force calculations, incorporate the coupling of the four legs, 
and impose the motor motion.

In the following, the indices letters $\mathbf{a}$ and $\mathbf{e}$ refer respectively to the actuation (motor) and the end-effector. 

In the algorithm, the four values of the actuation torque are introduced into the simulation as a vector of 
Lagrange multiplier $\boldsymbol{\lambda}_{\mathrm{a}}$. Furthermore, the motor positions in the simulation, 
$\boldsymbol{\delta}_{\mathrm{a}}$, is a function of the robot's position $\mathbf{q}$ 
(which is a concatenation of the leg positions: $\mathbf{q}_1,  ..., \mathbf{q}_4$).

![](assets/data/images/lab2-algorithm2.png){width=65%, .center}

To compute Equation 15 (in the algorithm above), it is more efficient to proceed with an indirect solution. 
We will decompose the movement at each time step by separating the contributions from the force $\mathbf{b}$, which is 
related to internal forces, external forces, and gravity (whose values we can compute), and the forces $\mathbf{H}_{\mathrm{a}}^T$ 
related to actuation (whose values are unknown and depend on the force required to satisfy the constraints).

$$
\mathbf{A}d\mathbf{q} = \mathbf{b} + \mathbf{H}_{\mathrm{a}}^T \boldsymbol{\lambda}_{\mathrm{a}} 
\Leftrightarrow
\left \{
\begin{array}{l}
d\mathbf{q} = d\mathbf{q}^{\mathrm{free}}  + d\mathbf{q}^{\lambda} \\ 
\mathrm{with}: \\
\mathbf{A}d\mathbf{q}^{\mathrm{free}} =  \mathbf{b} \leftrightarrow d\mathbf{q}^{\mathrm{free}} =  \mathbf{A}^{-1}\mathbf{b} \\
\mathbf{A}d\mathbf{q}^{\lambda} = \mathbf{H}_{\mathrm{a}}^T 
\boldsymbol{\lambda}_{\mathrm{a}} 
\leftrightarrow d\mathbf{q}^{\lambda}  = \mathbf{A}^{-1}\mathbf{H}_{\mathrm{a}}^T 
\boldsymbol{\lambda}_{\mathrm{a}}
\end{array}
\right .
$$

Thus, we can rewrite the kinematic constraint, 
$\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q} = \textcolor{red}{\mathbf{u}_{a}}$, 
as directly depending on the actuation force:

$$
\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}\left(d\mathbf{q}^{\mathrm{free}} + d\mathbf{q}^{\lambda}\right) = \textcolor{red}{\mathbf{u}_{a}} \Longleftrightarrow
$$

$$
\underbrace{
\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}}}_{\boldsymbol{\delta}_{\mathrm{a}}^{\mathrm{free}}} + 
\underbrace{\mathbf{H}_{\mathrm{a}}\mathbf{A}^{-1}\mathbf{H}_{\mathrm{a}}^T}_{\mathbf{W}_{\mathrm{aa}}} \boldsymbol{\lambda}_{\mathrm{a}} = \textcolor{red}{\mathbf{u}_{a}}
$$

This equation expresses the coupling of the actuation motion by the various torques via the compliance matrix $\mathbf{W}_{\mathrm{aa}}$, 
which represents the projection of the inverse matrix in the space of motor constraints.

The same way, we can rewrite 

$$
\textcolor{darkgreen}{\mathbf{y}_{e}} = \boldsymbol{\delta}_{\mathrm{e}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{e}} d\mathbf{q} 
$$

$$
\textcolor{darkgreen}{\mathbf{y}_{e}} =
\underbrace{
\boldsymbol{\delta}_{\mathrm{e}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{e}} d\mathbf{q}^{\mathrm{free}}}_{\boldsymbol{\delta}_{\mathrm{a}}^{\mathrm{free}}} +
\underbrace{\mathbf{H}_{\mathrm{e}}\mathbf{A}^{-1}\mathbf{H}_{\mathrm{a}}^T}_{\mathbf{W}_{\mathrm{ea}}} \boldsymbol{\lambda}_{\mathrm{a}}
$$

Combining equations above, we obtain a reduced formula of the linearized kinematics:

$$
\textcolor{darkgreen}{\mathbf{y}_{e}} = \boldsymbol{\delta}_{\mathrm{e}}^{\mathrm{free}} + \mathbf{W}_{\mathrm{ea}}\mathbf{W}_{\mathrm{aa}}^{-1} ( \textcolor{red}{\mathbf{u}_{a}} - \boldsymbol{\delta}_{\mathrm{a}}^{\mathrm{free}})
$$

$\mathbf{J}_{\mathbf{SR}} = \mathbf{W}_{\mathrm{ea}}\mathbf{W}_{\mathrm{aa}}^{-1}$ being the jacobian of the soft robot. 



:::::: exercise

**Exercise 1:**


Set up your robot, try different configuration of the legs and different connectors.

::::: group-grid 

**Motor n°0**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="exo1motor1orientation==counterclockwisedown"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="exo1motor1orientation==clockwisedown"}
:::: select exo1motor1orientation
::: option clockwisedown
::: option counterclockwisedown
::::

**Motor n°1**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="exo1motor2orientation==counterclockwisedown"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="exo1motor2orientation==clockwisedown"}
:::: select exo1motor2orientation
::: option clockwisedown
::: option counterclockwisedown
::::

**Motor n°2**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="exo1motor3orientation==counterclockwisedown"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="exo1motor3orientation==clockwisedown"}
:::: select exo1motor3orientation
::: option clockwisedown
::: option counterclockwisedown
::::

**Motor n°3**
![](assets/data/images/legs/blueleg-counterclockwisedown.png){data-condition="exo1motor4orientation==counterclockwisedown"}
![](assets/data/images/legs/blueleg-clockwisedown.png){data-condition="exo1motor4orientation==clockwisedown"}
:::: select exo1motor4orientation
::: option clockwisedown
::: option counterclockwisedown
::::

:::::

::::: group-grid 
**Connector**
![](assets/data/images/centerparts/bluepart.png){data-condition="exo1centerpart==bluepart"}
![](assets/data/images/centerparts/yellowpart.png){ data-condition="exo1centerpart==yellowpart"}
:::: select exo1centerpart
::: option bluepart
::: option yellowpart
::::
:::::

For each configuration, launch the corresponding simulation and apply movements to the motors. Observe the movement of the end effector. 
Specifically, analyze the difference between the model's predicted position and the robot's actual position. 
Also observe if and when some combinations of legs and connector configuration lead to mechanical instabilities.

1. What explains the instabilities?
2. What is the most *stable* configuration of the robot you have found (i.e. on which there is no mechanical instabilities)?

#runsofa-button(file="assets/labs/lab_inversekinematics/lab_inversekinematics.py", pyargs=["--legsName", "blueleg-direct", "--legsModel", "beam", "--legsPositionOnMotor", "exo1motor1orientation", "exo1motor2orientation", "exo1motor3orientation", "exo1motor4orientation", "--centerPartName", "exo1centerpart"])
::::::
:::::::
