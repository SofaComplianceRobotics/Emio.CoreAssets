::::: collapse Inverse Kinematics
## Inverse Kinematics

The goal of the inverse kinematics process is to find the inverse of the previously described relationship, i.e., to compute the motor command positions $\textcolor{red}{\mathbf{u}_{\mathrm{a}}} = \boldsymbol{f}^{-1}(\textcolor{darkgreen}{\mathbf{y}_{\mathrm{e}}})$. This means determining the motor inputs that result in the desired end-effector position.
There are several challenges in solving this inverse problem:

- **Non-uniqueness of the inverse**: The robot's structure is deformable, and as a result, the inverse relationship $\boldsymbol{f}^{-1}$ is not unique. Different motor positions $\mathbf{u}_{\mathrm{a}}$ can lead to the same end-effector position $\mathbf{y}_{\mathrm{e}}$, depending on the deformation of the robot's legs.
- **Internal forces and lack of analytical model**: The robot's kinematic model is based on internal forces within the deformable structure, and there is no general analytical model for $\boldsymbol{f}(\mathbf{u}_{\mathrm{a}})$. This makes it difficult to derive a closed-form expression for the inverse function, particularly because $\boldsymbol{f}(\mathbf{u}_{\mathrm{a}})$ is highly nonlinear.
- **Nonlinearity of the system**: As mentioned, $\boldsymbol{f}(\mathbf{u}_{\mathrm{a}})$ is a nonlinear function. Therefore, solving for the inverse kinematics requires setting up an optimization process that provides motor positions $\mathbf{u}_{\mathrm{a}}$ to minimize the distance with the desired end-effector position $\mathbf{y}_{\mathrm{e}}$.

To handle these challenges, we typically employ QP optimization techniques. 

![](assets/data/images/lab2-algorithm3.png){width=65%, .center}

With the indirect solving, the optimization presented in equation 20 (in the algorithm above) can be rewriten:

$$
\left \{
\begin{array}{l}
\mathbf{A}d\mathbf{q}^{\mathrm{free}}  =  \mathbf{b} \\
%%
\underset{\boldsymbol{\lambda}_{\mathrm{a}}}{min}
\frac{1}{2}(\boldsymbol{\delta}_{\mathrm{e}}(\mathbf{q}^{i-1}) + 
\mathbf{H}_{\mathrm{e}} d\mathbf{q}^{\mathrm{free}} 
+ \mathbf{W}_{\mathrm{ea}} \lambda_{\mathrm{a}}  
- \textcolor{darkgreen}{\mathbf{y}_{\mathrm{e}}})^2 \\
%%
\mathbf{A}d\mathbf{q}^{\lambda} = \mathbf{H}_{\mathrm{a}}^T 
\boldsymbol{\lambda}_{\mathrm{a}} 
\end{array}
\right .
$$

The advantage is that the optimization algorithm corresponds to convex optimization (i.e. Quadratic Programming - QP) 
on small matrices $\mathbf{W}_{\mathrm{ea}}$. If we develop the equation above, we obtain:

$$
\underset{\boldsymbol{\lambda}_{\mathrm{a}}}{min} (
\frac{1}{2} \lambda_{\mathrm{a}} \mathbf{W}_{\mathrm{ea}}^T \mathbf{W}_{\mathrm{ea}} \lambda_{\mathrm{a}}
+ \mathbf{W}_{\mathrm{ea}}^T(\boldsymbol{\delta}_{\mathrm{e}}(\mathbf{q}^{i-1}) + 
\mathbf{H}_{\mathrm{e}} d\mathbf{q}^{\mathrm{free}}   
- \textcolor{darkgreen}{\mathbf{y}_{\mathrm{e}}})\lambda_{\mathrm{a}}
)
$$

Remember that the relation between the motors torque and displacement 
is given by $\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}} + \mathbf{W}_{\mathrm{aa}}\boldsymbol{\lambda}_{\mathrm{a}} = \textcolor{red}{\mathbf{u}_{a}}$. Thus, to limit the course of the actuators we can add the following constraint to the QP:

$$
\textcolor{red}{\mathbf{u}_{min}} <=
\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}} + \mathbf{W}_{\mathrm{aa}}\boldsymbol{\lambda}_{\mathrm{a}}
<= \textcolor{red}{\mathbf{u}_{max}}
$$

and to constrain the actuators to a position $\textcolor{red}{\mathbf{u}_{0}}$ we can add the following constraint to the QP:

$$
\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}} + \mathbf{W}_{\mathrm{aa}}\boldsymbol{\lambda}_{\mathrm{a}}
= \textcolor{red}{\mathbf{u}_{0}}
$$

Each line of the two equations above constrains one of the actuators. 

In the case where the number of end-effectors is smaller than the number 
of actuators, we can have several solutions, but we can add a term $\epsilon \mathbf{W}_{\mathrm{aa}}$ to optimize the 
deformation energy [[Coevoet17]](https://inria.hal.science/hal-01649355/document) and achieve a unique solution.

In the tutorial, we propose you to implement the inverse kinematics using this QP optimization approach in Python. 
You will gain hands-on experience with solving real-world, nonlinear robotics problems. This exercise is valuable as 
it teaches how to handle constraints, explore a numerical optimization method, and deal with the complexities of soft 
robots in a practical context, fostering understanding of robot control and kinematics.

### Hands-on: Implement your own Optimization Program

To solve the inverse kinematics of Emio, we propose to write a Quadratic Program (QP). In this section you will
learn to write the QP system, understand singularity problems, and add constraints to the QP. Finally, you will use a solver
provided by the python library [qpsolvers](https://qpsolvers.github.io/qpsolvers/quadratic-programming.html#qpsolvers.solve_qp).

At this stage, the matrices $\mathbf{W}$ and vectors $d\mathbf{q}^{\mathrm{free}}$ and $\boldsymbol{\delta}(\mathbf{q}^{i-1})$ have been computed, and we want to solve the following optimization problem:

$$
\left \{
\begin{array}{l}
\underset{\boldsymbol{\lambda}_{\mathrm{a}}}{min} (
\frac{1}{2} \lambda_{\mathrm{a}} \mathbf{W}_{\mathrm{ea}}^T \mathbf{W}_{\mathrm{ea}} \lambda_{\mathrm{a}}
+ \mathbf{W}_{\mathrm{ea}}^T(\boldsymbol{\delta}_{\mathrm{e}}(\mathbf{q}^{i-1}) + 
\mathbf{H}_{\mathrm{e}} d\mathbf{q}^{\mathrm{free}}   
- \textcolor{darkgreen}{\mathbf{y}_{\mathrm{e}}})\lambda_{\mathrm{a}}
) \\
%%
\textrm{(optional)} \quad \textcolor{red}{\mathbf{u}_{min}} <=
\boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}} + \mathbf{W}_{\mathrm{aa}}\boldsymbol{\lambda}_{\mathrm{a}}
<= \textcolor{red}{\mathbf{u}_{max}} \\
%%
\textrm{(optional)} \quad \boldsymbol{\delta}_{\mathrm{a}}(\mathbf{q}^{i-1}) + \mathbf{H}_{\mathrm{a}}d\mathbf{q}^{\mathrm{free}} + \mathbf{W}_{\mathrm{aa}}\boldsymbol{\lambda}_{\mathrm{a}}
= \textcolor{red}{\mathbf{u}_{0}} 
\end{array}
\right .
$$

You will be asked to correctly identify the matrices from the system above to implement your own QP. 

:::: exercise

::: collapse {open} Set up Emio 

Take four <span style="color:blue">*blue legs*</span> and put them on each motor, as shown on the image. 
Pay a special attention to the orientation of the legs, it should be (counterclockwise / clockwise / counterclockwise / clockwise). 
Next, attach the <span style="color:blue">*blue connector*</span> at the tip of each leg, then fix
one <span style="color:green">*green marker*</span> on the center of the connector (as shown on the image).

![](assets/data/images/lab2-exercice2-emio.png){width=75% .center}

:::

**Exercise 2:**

Implement your own QP. Open the file `myQP_lab_inversekinematics.py` by clicking the *open* button, and follow the instructions step 
by step (todos):

![](assets/data/images/lab2-exercice2.png)

At each step, try your implementation by clicking the *SOFA* button (for this exercise, we won't connect the robot). Each time
you change the file `myQP_lab_inversekinematics.py`, you will need to close and relaunch the simulation for the changes to be taking into account.

#open-button(file="assets/labs/lab_inversekinematics/myQP_lab_inversekinematics.py")

#runsofa-button(file="assets/labs/lab_inversekinematics/lab_inversekinematics.py", pyargs=["--legsName", "blueleg", "--legsModel", "beam", "--legsPositionOnMotor", "counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown", "--centerPartName", "bluepart"])

::::
:::::
