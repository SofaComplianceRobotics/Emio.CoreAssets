:::::: collapse Static Analysis

## Static Analysis

Our approach is grounded in structural mechanics, which enables to account for both the geometric and material properties 
of the robot. To achieve a good level of generality, all models are derived from mechanical energy principles. 
We assume that whatever the configuration, the robot exhibits elastic behavior, meaning the energy considered is potential energy. 
Additionally, we assume that the robot moves slowly enough that kinetic energy can be neglected for the time being. 
This energy-based formulation is particularly well-suited to the weak formulations commonly used in continuum mechanics.  

Whatever the model, we suppose that the vector $\mathbf{q}$ represents the parameters of the motion (motion of the nodes in FEM, 
strains for Cosserat models) and $\mathcal{W}(\mathbf{q})$ is the potential energy of the deformation for the structure. 
The variation of the energy at the structural level can be discretized, meaning it can be decomposed as a sum of the 
energy variations at the level of each element $e$ (or each discrete rod), with $\sigma$ being the stress and $\mathbf{E}$ 
being the strain. 

$$
\partial \mathcal{W}(\mathbf{q}) = \int_{D} \boldsymbol{\sigma}^T  \partial \mathbf{E} \,dV
\approx \sum_e \int_e \boldsymbol{\sigma}^T(\mathbf{q}) \partial \mathbf{E}(\mathbf{q}) \,dV
$$

The internal forces $\mathbf{F}(\mathbf{q}) = \frac{\partial \mathcal{W}(\mathbf{q})}{\partial \mathbf{q} }$ are obtained by the derivative of this deformation potential energy.
We can make a parallel with the principle of virtual work, as the work created by $\partial \mathbf{q}$ needs to be equal to the variation of the strain energy: $\partial \mathcal{W}(\mathbf{q}) = \mathbf{F}(\mathbf{q})^T \partial \mathbf{q}$.

The configuration of the robot, given by $\mathbf{q}$ is obtained by solving the static equilibrium between these internal forces  $\mathbf{F}(\mathbf{q})$ and the external loads $\mathbf{F}_{ext}$, including the efforts exerted by the actuators. We can also add the forces created by the gravity $\mathbf{M}\mathbf{g}$. 

$$
\mathbf{F}(\mathbf{q}) + \mathbf{M}\mathbf{g} + \mathbf{F}_{ext} = \mathbf{0}
$$

In practice $\mathbf{F}(\mathbf{q})$ being non-linear, the computation of the equilibrium position is obtained by iterative resolution (see algorithm 1 below).

![](assets/data/images/lab1-algorithm1.png){width=65%, .center}

To model the various legs and their deformations, we propose three types of modeling of these internal forces:

- an FEM beam model, computed in global coordinates
- a Cosserat rod model, computed in local coordinates (strain space)
- a volume FEM with corotational linear tetrahedral elements

::::::
