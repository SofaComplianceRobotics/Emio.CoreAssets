import cv2 
import threading

class CameraViewer(threading.Thread):

    def __init__(self, parameter=None, comp_point_cloud=False, show_video_feed=True) -> None:

        print("Init Camera Viewer")
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def callback(self):

        print("Closing Camera Viewer")
        cv2.destroyWindow("Camera Preview")
        self.vc.release()

    def run(self):

        print("Starting Camera Viewer")
        cv2.namedWindow("Camera Preview")
        print("Capturing Camera Video")
        self.vc = cv2.VideoCapture(0)

        if self.vc.isOpened(): # try to get the first frame
            rval, frame = self.read()
            print("Camera opened")
        else:
            print("Camera not opened")
            rval = False

        while rval:
            print("Showing frame")
            cv2.imshow("Camera Preview", frame)
            rval, frame = self.read()
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break


def main():
    camera_viewer = CameraViewer()
    # camera_viewer.run()
    
if __name__ == '__main__':
    main()