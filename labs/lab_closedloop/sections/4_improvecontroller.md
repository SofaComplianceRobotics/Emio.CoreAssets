::::: collapse Improve the Integral Controller

## Improve the Integral Controller 

**Making the closed loop working.**
The main problem you encountered in the last step is called integrator windup.

It happens when the control cannot make the error converge to 0 because of physical limitation (workspace of the robot). 

To avoid that we need to detect the windup effect and prevent it to diverge. An easy way to do that is to compute the 
distance between the theoretical effector position and the target provided by the controller to the inverse model. 
When this difference is too big, recompute the target point to a fixed distance but the same relative direction 
from the effector position.

:::: exercise
**Exercise 6:**

1.  Try to implement this type of control **in simulation first**. 
2.  Try to reach points outside the workspace of the robot. 
3.  If everything goes well, try on the robot. 
4.  Write an open loop controller that relies on the QP solver. 
  
#open-button(file="assets/labs/lab_closedloop/myControl.py")

#runsofa-button(file="assets/labs/lab_closedloop/lab_closedloop.py")

#solution(file="solutions/lab_closedloop/answers.md", id="improvement")
::::
:::::