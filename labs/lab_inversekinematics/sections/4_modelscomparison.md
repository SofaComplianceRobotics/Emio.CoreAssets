:::::: collapse Models Comparison
## Models Comparison

In this section we propose to observe again the behavior of the *white leg*.
With a new configuration of the robot and using the solver provided by SOFA to solve its inverse kinematics, 
you will compare again the models, and conclude on the advantages and disadvantages of each approach. 

::::: exercise

::: collapse {open} Set up Emio 

Take four *white legs* and put them on each motor as shown on the image.
The orientations are the same as in exercise 1 and 2. 
Next, attach again the <span style="color:blue">*blue connector*</span> at the tip of each leg, and place
one <span style="color:green">*green marker*</span> on the top of the connector.

![](assets/data/images/lab2-exercice3-emio.png){width=75% .center}
:::

**Exercise 3:**

Try the three models with this setup of Emio. Move the effector target in the *x* direction. 

:::: select exo3model
::: option beam
::: option cosserat
::: option tetra
::::

1. What differences do you observe between the models?

Connect the simulation to the real robot and look at the error, i.e. the difference
between the two green and red spheres (you can also use the *Plotting* tab).

2. Which model gives the best simulation to real results?

#runsofa-button(file="assets/labs/lab_inversekinematics/lab_inversekinematics.py", pyargs=["--legsName", "whiteleg", "--legsModel", "exo3model", "--legsPositionOnMotor", "counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown", "--centerPartName", "bluepart"])

#solution(file="solutions/lab_inversekinematics/answers.md", id="exercise-3")
:::::
::::::
