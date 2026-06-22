:::: collapse Let's Try Emio

## Let's Try Emio

**1. Set up Emio:**
Take four <span style="color:blue">*blue legs*</span> and put them on each motor, as shown on the following image. 
Pay a special attention to the orientation of the legs, it should be from n°0 to n°3: counterclockwise, clockwise, counterclockwise, clockwise. 
Next, attach the <span style="color:blue">*blue connector*</span> at the tip of each leg. Plug the robot's USB cable to your computer.

![](assets/data/images/lab2-exercice2-emio.png){width="50%" class="center"}

**2. Run the simulation:**
Launch the simulation GUI by clicking the *SOFA* button below.   
On the GUI, click the *Play* button (center top) to start the simulation. 

|![](assets/data/images/play-pause-buttons.png){width="30%" class="center"}|
|:------------------------------------------------------------------------:|
|                 **Play / Pause, Step, and Reload buttons**                        |

Once you're ready, check that you are in the *Live Control* workbench and toggle the *Simulation / Robot* button, which is above the *Play* button, to connect and send 
the command to the robot.

**3. Pilot the robot:**
Navigate to the *Move* window, and use the sliders to move the effector's target.

#runsofa-button(file="assets/labs/introduction/introduction.py", pyargs=["-ln", "blueleg", "-lm", "beam", "-lp", "counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown", "-cn", "bluepart"])

::: collapse Troubleshooting

1. If you get the error message `ImportError: [libtk8.6.so]`, you need to install Tk, check the [requirements and the installation steps](https://docs-support.compliance-robotics.com/docs/v26.06/Users/EmioLabs/emio-labs-user-manual/#installation). 

2. On Windows, if you connect the robot to your computer and get the following error message `[ERROR] No serial port found with manufacturer = FTDI`. 
Try to install the [FTDI drivers](https://ftdichip.com/drivers/vcp-drivers/).

3. On Linux, when trying to connect the real robot, if you get a `[Errno 13] Permission denied: '/dev/ttyUSB0'` message. You need to give the serial port specific permissions to be accessed, you can follow [these instructions](https://docs-support.compliance-robotics.com/docs/v26.06/Users/Emio/getting-started-with-emio/#connecting-emio-to-your-computer).

:::

::::