:::::: collapse Comparison of Approaches

## Comparison of Approaches

:::: quiz
**Question 1:**
::: question What are the advantages of using beam models, compared to volume models?
Beam models simplify calculations compared to full three-dimensional models, reducing computation time 
and resources needed.
They are widely used in many civil and mechanical engineering applications, facilitating the analysis 
and design of structures such as bridges and buildings. In our case, beam models are well-suited to 
predict the behavior of a continuum robot, especially when the model is used for control purposes.
:::
::::


:::: quiz
**Question 2:**
::: question What are the disadvantages of using beam models, compared to volume models?
Beam models rely on assumptions that may not be valid for all situations, such as the assumption that 
cross-sections are undeformable and remain flat and perpendicular to the neutral axis (Bernoulli-Euler 
hypothesis). Timoshenko's theory accounts for shear deformation, but not all deformations of the 
cross-section are considered.
Beams are often not appropriate for structures with complex geometries or significant three-dimensional 
effects, where local deformations and stresses play a crucial role.
:::
::::

:::: quiz
**Question 3:**
::: question What can you tell about local and global parametrization?
Using a local parametrization (rates of bending, torsion, elongation) for beams allows for a more 
intuitive and compact modeling of internal deformations while parameterizing movement in a linear space. 
This approach can offer faster calculations and be closer to sensor information that could be placed on 
the beam (which would locally measure bending, torsion, or elongation). This can be compared to the
parametrization of articulated rigid robots in local coordinates.

Using a global parameterization (position of the nodes in space) simplifies the modeling of complex 
structures that connect a mesh of beams. This type of parameterization is often easier to implement 
for global structural analyses, contact management, or multi-physics coupling with other phenomena.
:::
::::

:::: quiz 
**Question 4:**
::: question Which model is the best suited for the blue leg? 
- [X] Cosserat
- [ ] Volume
- [X] Beam
:::
::::

#solution(file="assets/solutions/lab_models/answers.md", id="quiz")
::::::