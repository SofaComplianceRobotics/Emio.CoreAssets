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
|                 **Play / Pause and Step buttons**                        |

Once you're ready, toggle the *Simulation* button, which is above the *Play* button, to send 
the command to the robot.

**3. Pilot the robot:**
Navigate to the *Move* tab, and use the sliders to move the effector's target.

#runsofa-button(file="assets/labs/introduction/introduction.py", pyargs=["-ln", "blueleg", "-lm", "beam", "-lp", "counterclockwisedown", "clockwisedown", "counterclockwisedown", "clockwisedown", "-cn", "bluepart"])

::: collapse Troubleshooting

1. If you connect the robot to your computer and still get the following error message `[ERROR] No serial port found with manufacturer = FTDI`. 
Try to install the [FTDI drivers](https://ftdichip.com/drivers/vcp-drivers/).

2. On Ubuntu, when trying to connect the real robot, if you get a `[Errno 13] Permission denied: '/dev/ttyUSB0'` message. Run the following command in a terminal:
    ```console
    sudo chmod 777 /dev/ttyUSB0
    ```
   Make sure that the name of the USB port matches the one from the error message.
   
:::

::::