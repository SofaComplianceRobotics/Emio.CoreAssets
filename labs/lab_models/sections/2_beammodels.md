:::::: collapse Beam Models

## Beam FEM Model

This model was presented in [[Bieze21]](https://hal.science/hal-03028723/file/IJRR_EchelonIII_corrected%20(2).pdf), 
where a soft robot is created from a lattice of deformable beams. In this model, each beam connects two reference frames: 
two nodes whose position is given by a 3-dimensional vector (in the inertial frame), and orientation is given 
by a quaternion.

![](assets/data/images/beammodel.png){width=50%, .center}

Each of these nodes can have a rigid transformation with respect to its reference *DOF* frame. This facilitates 
the creation of lattices where two or more beams can be connected to the same DOF frame.

The proposed beams have a geometric support based on degree 3 splines between their nodes. This allows for good
geometric continuity and the calculation of their reference frame. Indeed, we use a corotational approach which
involves calculating an average frame for each element (here, we calculate it using a frame placed in the middle
of the beam). The deformation movements of each beam are first analyzed in this local frame to calculate the linear 
elastic forces. Then, these forces are placed back into the global frame; if there is no uniqueness between nodes 
and DOFs, we transfer the forces to the DOFs to assemble them with the forces of other beams on the same DOFs.

## Cosserat Model 
This model is an implementation of [[Renda16]](https://ieeexplore.ieee.org/document/7759808), where continuously deformable robots are studied
(see also [[Adagolodjo21]](https://hal.science/hal-03192168/document)). One of the
unique aspects of the model is that the motion parameters are calculated using a local parametric space, 
of the strain type. Thus, we parameterize the deformation movements of the rod by rates of bending, torsion,
elongation, or shearing. This allows us to easily decide not to simulate elongation and shearing, and 
such deformations will not appear on the rods. Each rod thus has 3 to 6 DOFs plus an additional 6 DOFs 
to define its base frame. We can have multiple rods in series starting from the same base. In the basic 
implementation in SOFA, the number of DOFs depends on the number of elementary rods arranged in series. 

In a more advanced implementation, we can use polynomial interpolation along a series of rods to further
reduce the number of DOFs. Once the movements of these DOFs are known, we can reconstruct the configuration 
of the rods through the calculation of the direct geometric model. 
However, since inertial forces and contact forces are more easily expressed in the global frame, this model 
requires bringing these values back through a recurrence from the end of the rod to its base.

## Parameters

[Young's modulus](https://en.wikipedia.org/wiki/Young%27s_modulus) (unit of pressure Pa), also called the modulus of elasticity, is a mechanical property of solid materials that 
quantifies their tensile or compressive stiffness when subjected to lengthwise force. It represents the modulus of 
elasticity for tension or axial compression. Young's modulus is defined as the ratio of the applied stress (force per unit area) 
to the resulting axial strain (displacement or deformation) within the material's linear elastic region.

![](assets/data/images/poissonRatio.svg){width=19% align=right style=margin:15px}

[Poisson's ratio](https://en.wikipedia.org/wiki/Poisson%27s_ratio) measures the deformation (expansion or contraction) of a material in directions perpendicular 
to the applied load. For small deformations, Poisson's ratio is the ratio of transverse elongation to axial compression. 
Most materials have Poisson's ratio values between in 0.0 and 0.5.

Soft materials, like rubber, with a bulk modulus 
much higher than the shear modulus, have Poisson's ratios near 0.5. Open-cell polymer foams have Poisson's ratios 
near zero due to cell collapse under compression. Typical solids have Poisson's ratios in the range of 0.2 to 0.3.

## Hands-on

Now you will play with the simulation and compare the deformations with the ones of the real device. 
You will see which parameters influence the most the beam and Cosserat models, 
and finally estimate the parameters that improve the models' fidelity.


::::: exercise
::: collapse {open} Set up Emio 
Take the <span style="color:blue">*blue leg*</span> and put it on the *motor n°0* (clockwise down as shown on the image). 
Next, attach the <span style="color:grey">*grey cube*</span> at the tip of the leg, then place
two <span style="color:green">*green markers*</span> on the leg: one in the middle of the leg and the second at the tip,
just above the cube.

![](assets/data/images/lab1-exercice1-leg.png){.center width=50%}

:::


**Exercise 1:**

Once setup, choose a model between *beam* and *cosserat* in the drop-down menu below:

:::: select modelsexo1
::: option beam 
::: option cosserat 
::: option tetra
::::

Launch the simulation, make sure that the markers you put on the leg match the 
markers in the simulation, then change the motor's position. Observe the deformation differences 
between the simulation and the real leg. Adjust the parameters until the simulation accurately 
mirrors the deformation of the real device.

1. Which parameters influences the most the deformation of the leg in this configuration?  
2. Which parameters did you choose to change and why?

After determining the appropriate values, save them in the file `myparameters.py`. Click the *open* button, enter 
the values, and save the changes (ctrl + s).

#open-button(file="assets/labs/lab_models/myparameters.py")

#runsofa-button(file="assets/labs/lab_models/lab_models.py", pyargs=["blueleg", "modelsexo1"])

#solution(file="assets/solutions/lab_models/answers.md", id="parameters")

:::::
::::::
