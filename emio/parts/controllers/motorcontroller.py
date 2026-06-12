import Sofa
import Sofa.ImGui as MyGui
from emioapi.emiomotors import EmioMotors
from emioapi import EmioAPI
import threading
import time

# When reloading the scene in SOFA, the modules are first unloaded and then reloaded. 
# This allows to update the python code without restarting the entire application.
# However, cv2 causes issues when being reloaded, so we exclude it from the process.
import SofaRuntime
if not "cv2" in SofaRuntime.__SofaPythonEnvironment_modulesExcludedFromReload:
    SofaRuntime.__SofaPythonEnvironment_modulesExcludedFromReload.append("cv2")
    

def connectRobot(emiomotors: EmioMotors, stopevent: threading.Event):
    """
    This function runs in a separate thread to check the connection status of the robot.
    It will open the connection if the simulation/robot toggle button from the GUI is on and the robot is not connected,
    and close the connection if the toggle is off and the robot is connected.
    """
    emioConnected = False
    
    while not stopevent.is_set():
        emioConnected = emiomotors.is_connected
        if MyGui.getRobotConnectionToggle() and not emioConnected:
            try:
                index = emiomotors.findAndOpen(device_name=MyGui.MyRobotWindow.getSelectedPort())
                if index == -1:
                    Sofa.msg_error("MotorController", "Could not find or connect Emio robots. Please check the connection.")
                    MyGui.MyRobotWindow.updateAvailablePorts()
                MyGui.setRobotConnectionToggle(index >= 0 ) # GUI toggle with the current connection status
            except Exception as e:
                Sofa.msg_error("MotorController", str(e))
                MyGui.setRobotConnectionToggle(False)
                MyGui.MyRobotWindow.updateAvailablePorts()
                emiomotors.close()
        elif not MyGui.getRobotConnectionToggle() and emioConnected:
            emiomotors.close()

        time.sleep(2) # wait 2 seconds before checking again

    if emioConnected:
        emiomotors.close()
    

stopThreadEvent = threading.Event()
connectionThread = None

def isConnectionThreadAlive():
    global connectionThread
    global stopThreadEvent
    return connectionThread and connectionThread.is_alive()

class MotorController(Sofa.Core.Controller):
    
    def __init__(self, jointActuators, *args, **kwargs):
        Sofa.Core.Controller.__init__(self, *args, **kwargs)

        self.name = "MotorController"
        self.jointActuators = jointActuators
        self.emiomotors = EmioMotors()
        MyGui.MyRobotWindow.listAvailablePortsCallback(self, "listAvailablePortsCallback")

        # Connection thread
        MyGui.MyRobotWindow.updateAvailablePorts() # Initial population of available ports
        if isConnectionThreadAlive(): # stop the thread before continuing
            self.stopConnectionThread()

        self.startConnectionThread()

    def __del__(self):
        if isConnectionThreadAlive():
            self.stopConnectionThread()

    def startConnectionThread(self):
        global connectionThread
        global stopThreadEvent

        connectionThread = threading.Thread(target=connectRobot, args=[self.emiomotors, stopThreadEvent])
        connectionThread.daemon = True
        connectionThread.start()

    def stopConnectionThread(self):
        global connectionThread
        global stopThreadEvent

        stopThreadEvent.set()
        connectionThread.join()
        connectionThread = None
        stopThreadEvent.clear()

    def onAnimateEndEvent(self, _):
        """
        This function is called at the end of each animation step.
        It checks the connection status of the robot and updates the joint angles if connected.
        """
        if MyGui.getRobotConnectionToggle() and self.emiomotors.is_connected:
            angles = []
            for joint in self.jointActuators:
                if joint is not None:
                    angles.append(joint.value)
                else:
                    angles.append(0)
            try:
                self.emiomotors.angles = angles
            except Exception as e:
                Sofa.msg_error("MotorController - onAnimate", str(e))
                MyGui.setRobotConnectionToggle(False)
                self.emiomotors.close()

    def listAvailablePortsCallback(self) -> list[str]:
        """
        Update the list of available EMIO devices in the GUI.
        """
        ports = EmioAPI.listEmioDevices()  
        if ports is not None and len(ports) != 0:
            return ports
        return ["No Emio robots found"]   

