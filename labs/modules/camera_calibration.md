::: collapse Camera Calibration

## Calibrating the Camera
The calibration allows to calculate the transform from the camera image to 3D points into the simulation reference frame. The Emio API (included with Emio Labs) comes with a default calibration, but it can vary based on if the camera has been moved. 

If you notice a large difference between the simulation and reality markers, you might need to re-calibrate the camera.

### Set up Emio for Calibration

<img src="assets/data/images/calibration_emio_setup.png" style="margin:25px;float:right;" width="38%" >

You will need:

- (1) the Aruco marker 
- (2) two green markers
- (3) the blue elevators to raise the platform

Then, follow these steps:
1. Raise the platform with the blue elevators.
2. Place the Aruco marker on the platform, arrow facing the camera.
3. Insert two green markers into the Aruco marker slots.
4. Connect Emio to the computer and power supply.
5. Turn on Emio.

The set up should look like the picture on the right.
<br/>

### Start the Calibration

1. Open the calibration scene
2. Press the _Play_ button to start the simulation
3. Toggle the robot connection button to connect to the robot

#runsofa-button("assets/utils/calibrationscene.py")

### Calibration Process

The process will start by opening several windows, including a _Calibration_ window and a _HSV_ window.

| ![](assets/data/images/calibration_window.png){width=90% .center} | ![](assets/data/images/calibration_hsv.png){width=90% .center} |
|:-----------------------------------------------------------------:|:--------------------------------------------------------------:|
|**The _Calibration_ window displays the corners and other points detected by the camera.**|**The _HSV_ window displays the 3D position of the two markers in the frame of the camera (first line) and in the simulation frame (second line).**|

The calibration ends when the _Calibration_ window closes and the _HSV_ window displays the position of the two markers.

To make sure the calibration is successful, you can check the simulation coordinates of the markers in the HSV window:
- The top marker should be at around `(32, -230, 32)`
- The bottom marker should be at `(-32, -230, -32)`

In the simulation, the green markers (_i.e._ what the camera is tracking) should be at the same positions as the red markers (_i.e._ theoretical positions). The actual error for each marker can be seen in the _Information_ collapsible menu in the _My Robot_ window. You can expect an error of around 2-4 mm for each marker.

Once the calibration is complete, you can close the SOFA window. The saved calibration will be used for all subsequent use of the camera.

![](assets/data/images/calibration_simulation.png){width=90% .center}

:::