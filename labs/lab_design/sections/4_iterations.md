:::: collapse Iteration on the Leg Design to Meet the Specifications
### Iteration on the Leg Design to Meet the Specifications

So far, we performed only one design iteration through steps 1 to 4. 
Model-based design processes are generally iterative. 
The performances obtained for a given design are compared to the desired ones, and the design parameters are changed by the user to reduce the error (similarly to a closed-loop control scheme). 
This iteration process can be partly to fully automated using off-the-shelf numerical optimization methods such as gradient-descent. 
Note that using these tools may require additional work, such as reformulating the soft robot model and the optimization problem to obtain a mathematical form suitable for optimization (quadratic cost function to ensure convexity for example). 
Other methods like evolutionary algorithms can also be used to search the design space of parametric designs efficiently. 
Instead of optimizing a single candidate, these methods evaluate populations of candidates which evolve over generations. 
In our case, to avoid going deep on the problem formulation and to get intuition on how the design parameters affect the finger performances, we will iterate manually on the design parameters. 

::: exercise
**Exercise 2:**

Repeat the design process until the specifications are met. 
- What are the values of **w** and **t** ? 
- What is the final curved profile of the leg ? 
- How intricate is it to find the optimal design parameters manually?

Some advices: 
- Try to vary one parameter at a time (at least at the beginning), to learn its influence on the robot behavior. 
- Keep notes of what designs you already tried. 

#runsofa-button(file="assets/labs/lab_design/lab_design.py", pyargs=["rigid"])
:::
::::
