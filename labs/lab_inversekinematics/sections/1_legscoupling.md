::::::: collapse Coupling of the legs
## Coupling of the legs

As described in the previous lab, the robot's legs are modeled as deformable structures. These legs can be grouped 
in various configurations using connectors. The aim of this lab is to place the legs in two different 
positions on the motor (clockwise or counterclockwise), and test different effectors. 
Certain configurations may result in mechanical instabilities, primarily due to leg buckling. 
This hands-on experiment will enable you to observe that some configurations are mechanically more stable than others 
and that, sometimes, several position of the effector $\mathbf{y}_{e}$ can be found for the same motor positions $\mathbf{u}_{a}$.

Next, we propose to introduce the mathematical modeling of leg coupling using three different modeling approaches. 
In each case, the objective is to constrain the degrees of freedom (DOF) of the leg ends to match those of the effector. 
Note that in the case of FEM, the DOF are the unkonwn positions (nodes), in Cosserat models, they correspond to the strains.
For simplicity, we assume in the following that the robot has only two actuated legs, although in reality it has four. 

### Case 1: Absolute Coordinates 

To enforce this equality, the simplest case arises when we work with the DOF in absolute coordinates in space. 
In such a case, the idea is to select the degrees of freedom at the end of the leg (in this case,
$\mathbf{I}_1$ and $\mathbf{I}_2$) and equalize them together with the end-effector motion at each step.

$$
 \left\{ 
 \begin{array}{l}
 \mathbf{A}_1 d\mathbf{q}_1 = \mathbf{b}_1  \ \ \text{leg 1}  \\
 \mathbf{A}_2 d\mathbf{q}_2 = \mathbf{b}_2  \ \ \text{leg 2}  \\
 \text{with} \\
 \underbrace{\left [ 0 ... 0 \ I \  0 ... 0  \right ]}_{\mathbf{I}_1} d\mathbf{x}_1 = 
 \underbrace{\left [ 0 ... 0 \ I \  0 ... 0  \right ]}_{\mathbf{I}_2}
 d\mathbf{x}_2 = d\mathbf{y}_e
 \end{array}
 \right.
$$

In this case, we can reorder the equations to equalize the components of $\mathbf{q}_1$ and $\mathbf{q}_2$ corresponding 
to the end DOF of the legs that need to be matched.

$$
\underbrace{
    \left[  
    \begin{array}{lll}
    \mathbf{A}_1 & \mathbf{A}_1 & 0 \\
    0 & \mathbf{A}_1 + \mathbf{A}_2 & \mathbf{A}_2 \\
    0 & \mathbf{A}_2 & \mathbf{A}_2  
    \end{array}
    \right]
}_{\mathbf{A}}
\underbrace{
    \left[  
    \begin{array}{l}
        d\mathbf{q}_1^{\neq} \\
        d\mathbf{q}_1^{=} = d\mathbf{q}_2^{=} \\
        d\mathbf{q}_2^{\neq}
    \end{array}
    \right]
}_{d\mathbf{q}}    
    =
\underbrace{
    \left[  
    \begin{array}{l}
        \mathbf{b}_1 \\
        \mathbf{b}_1^{=} + \mathbf{b}_2^{=} \\
        \mathbf{b}_2 
    \end{array}
    \right]
}_{\mathbf{b}}    
$$

In practice this case is only implemented with FEM beams.

### Case 2: Lagrange Multipliers

In the second and third cases, the absolute position of each leg end, $\mathbf{x}_1$ and $\mathbf{x}_2$, is derived kinematically from the DOF $\mathbf{q}_1$ and $\mathbf{q}_2$, respectively with a kinematic function $\mathbf{x}_1 = \boldsymbol{\delta}_1(\mathbf{q}_1)$ and $\mathbf{x}_2 = \boldsymbol{\delta}_2(\mathbf{q}_2)$.
This allows us to write the equality in terms of the effector's position $\mathbf{y}_e = \mathbf{x}_1  = \mathbf{x}_2$.
In $\boldsymbol{\delta}_1$ and $\boldsymbol{\delta}_2$ we take into account the offset of the end of the leg in relation to the center of the end effector.

$$
\left\{ 
\begin{array}{l}
d\mathbf{x}_1  = \mathbf{H}_1 d\mathbf{q}_1  = d\mathbf{y}_e \\
d\mathbf{x}_2  = \mathbf{H}_2 d\mathbf{q}_2 = d\mathbf{y}_e
\end{array}
\right.
$$

with $\mathbf{H}_1  = \frac{\partial  \delta_1}{\partial \mathbf{q}_1}$ and $\mathbf{H}_2  = \frac{\partial  \delta_2}{\partial \mathbf{q}_2}$, the direction of the effort applied on the FEM nodes.

so we need to impose the kinematic constraint:
$$
 \mathbf{H}_1 d\mathbf{q}_1 = 
 \mathbf{H}_2 d\mathbf{q}_2 
$$

In Case 2, Lagrange multipliers are used to enforce position constraints, which increases the system's size.

$$
\underbrace{
    \left[  
    \begin{array}{lll}
    \mathbf{A}_1 & 0 & \mathbf{H}_1^T \\
    0 & \mathbf{A}_2 & -\mathbf{H}_2^T \\
    \mathbf{H}_1 & -\mathbf{H}_2^T & 0  
    \end{array}
    \right]
}_{\mathbf{A}}
\underbrace{    
    \left[  
    \begin{array}{l}
        d\mathbf{q}_1 \\
        d\mathbf{q}_2 \\
        \boldsymbol{\lambda}
    \end{array}
    \right]
}_{d\mathbf{q}}    
    =
\underbrace{
    \left[  
    \begin{array}{l}
        \mathbf{b}_1 \\
        \mathbf{b}_2 \\
        0
    \end{array}
    \right]
}_{\mathbf{b}}   
$$

### Case 3: Penalty Approach

In Case 3, a penalty method is applied. It consists of creating a coupling forces to impose the kinematic constraint.

$$
 \left\{ 
 \begin{array}{l}
 \mathbf{A}_1 d\mathbf{q}_1 = \mathbf{b}_1 + \mathbf{f}_1 \ \ \text{leg 1} \\
 \mathbf{A}_2 d\mathbf{q}_2 = \mathbf{b}_2 + \mathbf{f}_2 \ \ \text{leg 2} \\ 
 \mathbf{H}_1 k(\mathbf{H}_1 d\mathbf{q}_1 - 
 \mathbf{H}_2 d\mathbf{q}_2 )  = -\mathbf{f}_1 \\
 \mathbf{H}_2 k(\mathbf{H}_1 d\mathbf{q}_1 - 
 \mathbf{H}_2 d\mathbf{q}_2 )  = \mathbf{f}_2
 \end{array}
 \right.
$$

While this approach keeps the system size constant, additional coupling terms may appear in the matrix.

$$
\underbrace{
    \left[  
    \begin{array}{ll}
    \mathbf{A}_1 + \mathbf{H}_1^T k \mathbf{H}_1 & -\mathbf{H}_1^T k \mathbf{H}_2 \\
    -\mathbf{H}_1^T k \mathbf{H}_2 & \mathbf{A}_2 + \mathbf{H}_2^T k \mathbf{H}_2 
    \end{array}
    \right]
}_{\mathbf{A}}
\underbrace{   
    \left[  
    \begin{array}{l}
        d\mathbf{q}_1 \\
        d\mathbf{q}_2 
    \end{array}
    \right]
}_{d\mathbf{q}}    
    =
\underbrace{
    \left[  
    \begin{array}{l}
        \mathbf{b}_1 \\
        \mathbf{b}_2 
    \end{array}
    \right]
}_{\mathbf{b}}       
$$

In all three cases, the result is a linear system that must be solved at each time step, similar to the static equilibrium 
equations used for individual leg kinematics. Lagrange Multiplier and Penalty approach are more generic as it does not 
require to use absolute coordinate system, like for the proposed Cosserat Model. 

:::::::
