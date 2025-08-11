# Lab Closed Loop

::: highlight
##### Overview

This lab is dedicated to control. Its goals are to make you understand:

1. When and why a closed loop control scheme is required for a given application.
2. What are the effects of the different parameters of the controller.
3. The limitation of the proposed approach and what has to be done to overcome it.
4. Give some insight of what could be achieved with more time.
:::

::: collapse {open} Set up Emio  for the Lab
## Set up Emio

In this lab session, we will use only the following configuration: Emio with the <span style="color:blue">*blue legs*</span>,
the <span style="color:blue">*blue connector*</span>, and the <span style="color:green">*green marker*</span>:

![](assets/data/images/lab2-exercice2-emio.png){width=75% .center}

In the provided simulation, we now consider the effect of a disturbance acting at the tip of the robot. This force can be simulated in the provided scene.
:::

#include(assets/labs/lab_closedloop/sections/1_openloopcontrol.md)
#include(assets/labs/lab_closedloop/sections/2_proportionalcontroller.md)
#include(assets/labs/lab_closedloop/sections/3_integralcontroller.md)
#include(assets/labs/lab_closedloop/sections/4_improvecontroller.md)