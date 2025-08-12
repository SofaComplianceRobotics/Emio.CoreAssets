::::: collapse Open Loop Control
## Open Loop Control

**Open loop accuracy.** 
The idea of inverse model based control is to rely on Inverse Kinematic method to simplify the control loop. The principle is depicted in the following figure:

|  ![](assets/data/images/OL-principle.png)   | 
|:-------------------------------------------:|
| **Inverse-model-based Open loop principle** |

If we consider the following quasi-static model:
$$q_{k+1}=q_k + \delta_{free}(q_k)+W(q_k)\lambda_k$$
where $q_k$ is the effector positon and $\lambda_k$ the efforts. 
If we consider the following linearising control:
$$\lambda_k=W(q_k)^{-1}(q_t-q_k - \delta_{free}(q_k)))$$
the results is given by:
$$q_{k+1}=q_t$$

For the implementation, instead of using the inverse of the matrix we will prefer to solve an optimisation problem (as seen in previous labs) which allows to solve the problem even if $W$ is not square and allows us to add constrains.

In order to implement that controller, one needs to write the inverse problem `assets/labs/lab_closedloop/myQP_lab_closedloop_.py`  and to write the open loop controller `assets/labs/lab_closedloop/myControl.py`. The connexions are depicted here:

|  ![](assets/data/images/OL-implementation.png)   | 
|:------------------------------------------------:| 
| **Inverse-model-based Open loop implementation** |


:::: exercise
**Exercise 1:**

Open the script `assets/labs/lab_closedloop/myControl.py` by clicking on the *open* button below, and have
a glance at the content. Read the descriptions and try to understand what the script does 
and how it works. 

#open-button("assets/labs/lab_closedloop/myControl.py")
::::

:::: exercise
**Exercise 2:**

Write the QP optimization problem. 

#open-button("assets/labs/lab_closedloop/myQP_lab_closedloop.py")
::::

:::: exercise
**Exercise 3:**

Choose some target points and try to reach them. Then: 
1. Observe the error on the plots.
2. Conclude about the accuracy of the open loop controller.
3. Try to reach points outside the workspace of the robot.

#runsofa-button("assets/labs/lab_closedloop/lab_closedloop.py")
::::

:::::
