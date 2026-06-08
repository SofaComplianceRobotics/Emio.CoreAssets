:::: collapse Software GUI
## Software GUI

We use the simulation framework [SOFA](https://www.sofa-framework.org/) to model, simulate, and solve the inverse kinematics of Emio. The GUI (SOFA Robotics), developed by Compliance Robotics on top of SOFA, 
enables intuitive piloting and programming of the robot.

The GUI features three main components: a simulation 3D viewport, where you can visualize the simulated robot, a series of windows that
provide various functionalities, and workbenches. 

Workbenches can be considered as a set of windows and functionalities specially grouped for a certain task. There are three workbenches:
1. **Scene Editor** - For building and editing the scene.
2. **Simulation Mode** - For running the simulation.
3. **Live Control** - For connecting to and controlling the real robot with the finalized scene.

|![](assets/data/images/workbenches.png){width="45%" class="center"}|
|:-----------------------------------------------------------------------:|
|                 **Workbenches button**                    |

There are several windows, we will only list here the most important ones, for the labs:

1. **My Robot**: Access information and settings related to the simulation and Emio. Also contains a connection section where you can select the port to connect to the real robot, and check its status.
2. **Move**: Directly control the TCP (tool center point) target or adjust the position of motors.
3. **Program**: Develop robot programs by adding waypoints on a timeline that corresponds to simulation time.
4. **Plotting**: Some labs include plotting data for analysis purposes.

| ![](assets/data/images/emio-simulationgui.png) |
|:----------------------------------------------:|
|           **Screenshot of the GUI**            |

From the *Live Control* workbench, the *Simulation* button toggles the connection between the simulation and the physical robot. In simulation mode, the robot remains stationary, providing a safe environment to test your programs. Before deploying your programs on the real robot, ensure they are
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