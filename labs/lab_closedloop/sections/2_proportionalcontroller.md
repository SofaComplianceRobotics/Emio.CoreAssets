::::: collapse Proportional Controller Closed Loop 
## Proportional Controller Closed Loop

**Inverse model-based control principle.** 
The problem of the open loop controller is that the model is just an approximation of the reality. Some uncertainties and disturbances makes this type of control innacurate and sensitive to the environement.

To solve this problem, on can use to close the control loop by exploiting a sensor feedback in the control scheme:

|   ![](assets/data/images/CL-principle.png)    | 
|:---------------------------------------------:|
| **Inverse-model-based Closed loop principle** |

This schemes allows to take new actions according to what happens in reality.
We will keep the idea of inverse model based control to simplify the behavior of the robot:
$$q_{k+1}=q_t + f(d_k)$$
where $d_k$ is the disturbance (badly modeled things and interactions with the environment) that is represented by a force applied at the effector.

The controller that we will implement will check the error between the user target and sensor feedback and will add a shift to $q_t$ each time an error is detected (proportial action in the direction of the error):
$$ q_t = q_{user} + k_p * \varepsilon $$

This controller is composed of a feedforward $q_{user}$ and a feedback part $k_p * \varepsilon$. $varepsilon$ is the error between the target provided by the user and the current location of the effector.

|   ![](assets/data/images/CL-implementation.png)    | 
|:--------------------------------------------------:| 
| **Inverse-model-based Closed loop implementation** |

::: highlight
#icon("warning") **Warning:** Be careful with these controllers as they can be unstable if they are badly implemented or tunned.
**A good practice is to check in simulation first.**
:::

:::: exercise

**Exercise 4:**

1.  Try to implement this type of control **in simulation first** and then test it on the robot, observe the error. 
2.  Try to disturb the robot during the experiment, observe the reaction of the robot for different values of the control gain. 
3.  Try to reach points outside the workspace of the robot. 
4.  Try to increase the control gain. 
5.  Conclude on what to do next. 
  
#open-button(file="assets/labs/lab_closedloop/myControl.py")

#runsofa-button(file="assets/labs/lab_closedloop/lab_closedloop.py")

#solution(file="assets/solutions/lab_closedloop/answers.md", id="proportional")
::::

:::::
