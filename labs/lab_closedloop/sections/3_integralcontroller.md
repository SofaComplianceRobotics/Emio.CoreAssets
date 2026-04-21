::::: collapse Integral Controller Closed Loop 

## Integral Controller Closed Loop 

**Integral action principle.** 
In order to remove completely the steady state error, it is usual to incorporate an integral action. For sake of 
simplicity, we propose to implement this integral action alone (remove the previous controller).

The principle is to give a velocity to the Qp target $q_t$ in the direction of the error so that the $q_t$ will 
'search' for the right value that compensate the steady state error. The initial value of the $q_t$ should be an 
admissible value for the robot otherwise the robot might go crazy.

:::: exercise

**Exercise 5:**

1.  Try to implement this type of control **in simulation first** and then test it on the robot, observe the error. 
2.  Try to disturb the robot during the experiment, observe the reaction of the robot for different values of the control gain. 
3.  Try to reach points outside the workspace of the robot. 
4.  Try to increase the control gain. 
5.  Conclude on what to do next. 
  
#open-button(file="assets/labs/lab_closedloop/myControl.py")

#runsofa-button(file="assets/labs/lab_closedloop/lab_closedloop.py")

#solution(file="solutions/lab_closedloop/answers.md", id="integral")
::::

:::::