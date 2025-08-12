:::: collapse Software GUI
## Software GUI

We use the simulation framework [SOFA](https://www.sofa-framework.org/) to model, simulate, and solve the inverse kinematics of Emio. The GUI, developed by Compliance Robotics on top of SOFA, 
enables intuitive piloting and programming of the robot.

The GUI features two main components: a simulation 3D viewport, where you can visualize the simulated robot, and a series of tabs that
provide various functionalities. These tabs allow you to program the robot or directly control its movements:

1. **My Robot**: Access information and settings related to the simulation and Emio.
2. **Move**: Directly control the TCP target or adjust the position of motors.
3. **Program**: Develop robot programs by adding waypoints on a timeline that corresponds to simulation time.
4. **Plotting**: Some labs include plotting data for analysis purposes.

| ![](assets/data/images/emio-simulationgui.png) |
|:----------------------------------------------:|
|           **Screenshot of the GUI**            |

The *Simulation* button toggles the connection between the simulation and the physical robot. In simulation mode, the robot remains
stationary, providing a safe environment to test your programs. Before deploying your programs on the real robot, ensure they are
thoroughly tested in simulation mode to avoid any potential issues.

|![](assets/data/images/simulation-toggle.png){width="20%" class="center"}|
|:-----------------------------------------------------------------------:|
|                 **Simulation / Robot switch button**                    |

::: highlight
#icon("info-circle")  **Note:** As previously mentioned, throughout the lab sessions, you will receive instructions to set up Emio in specific configurations.
Some exercises use the simulation software described above. You will need to select options to configure Emio; 
these selections affect the simulation setup. Make sure that the simulation matches the real robot.
:::
::::