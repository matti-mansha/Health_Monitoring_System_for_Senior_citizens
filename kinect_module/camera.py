import numpy as np
import cv2
from pykinect import nui
import os

class Camera:
    def __init__(self):
        self.kinect = nui.Runtime()
        self.file_name = "text.txt"
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.file = open(self.file_name, "a")

    def video_handler_function(self, frame):
        # Convert video frame to numpy array
        video = np.empty((480, 640, 4), np.uint8)
        frame.image.copy_bits(video.ctypes.data)

        # Get skeleton data for each tracked skeleton in the frame
        frame_points = []
        frame = self.kinect.skeleton_engine.get_next_frame()
        for skeleton in frame.SkeletonData:
            if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
                for joints in skeleton.SkeletonPositions:
                    x, y, z = round(joints.x, 7), round(joints.y, 7), round(joints.z, 7)
                    frame_points.append([x, y, z])
                if len(frame_points) != 0:
                    self.file.write(str(frame_points) + "\n")
        
        # Display video frame
        cv2.imshow('KINECT Video Stream', video)

    def run(self):
        try:
            self.kinect.skeleton_engine.enabled = True
            self.kinect.video_frame_ready += self.video_handler_function
            self.kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
        except Exception as e:
            print("Error: {}".format(e))
            self.kinect.close()
            self.file.close()
            cv2.destroyAllWindows()
            return
        
        cv2.namedWindow('KINECT Video Stream', cv2.WINDOW_AUTOSIZE)

        while True:
            key = cv2.waitKey(1)
            if key == 27: break

        self.kinect.close()
        self.file.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    camera = Camera()
    camera.run()
