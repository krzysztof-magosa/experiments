#! /usr/bin/env python2.7

import numpy as np
import cv2

class App:
    camera = None
    windows = {
        "camera": "Camera",
        "hsv": "HSV",
        "mask": "Mask",
        "trackbars": "Trackbars"
    }
    trackbars = {
        "min_h": "Min Hue",
        "max_h": "Max Hue",
        "min_s": "Min Saturation",
        "max_s": "Max Saturation",
        "min_v": "Min Value",
        "max_v": "Max Value"
    }
    keys = {
        "quit": ord('q')
    }

    def on_trackbar_change(self, value=None):
        for (key, name) in self.trackbars.items():
            self.values[key] = float(cv2.getTrackbarPos(name, self.windows["trackbars"]))

        print(self.values)
    
    def init_camera(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        self.camera.set(cv2.cv.CV_CAP_PROP_FPS, 25)

    def init_windows(self):
        cv2.namedWindow(self.windows["camera"])
        cv2.namedWindow(self.windows["hsv"])
        cv2.namedWindow(self.windows["mask"])
        cv2.namedWindow(self.windows["trackbars"], cv2.WINDOW_NORMAL)

    def init_trackbars(self):
        cv2.createTrackbar(self.trackbars["min_h"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)
        cv2.createTrackbar(self.trackbars["max_h"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)
        cv2.createTrackbar(self.trackbars["min_s"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)
        cv2.createTrackbar(self.trackbars["max_s"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)
        cv2.createTrackbar(self.trackbars["min_v"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)
        cv2.createTrackbar(self.trackbars["max_v"], self.windows["trackbars"], 0, 255, self.on_trackbar_change)

        """ ??? """
        self.values = {}
        self.on_trackbar_change()
        
    def __init__(self):        
        self.init_camera()
        self.init_windows()
        self.init_trackbars()
        
    def run(self):
        while True:
            ret, frame = self.camera.read()

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            m1 = (self.values["min_h"], self.values["min_s"], self.values["min_v"])
            m2 = (self.values["max_h"], self.values["max_s"], self.values["max_v"])
            frame_mask = cv2.inRange(frame_hsv, np.array(m1), np.array(m2))

            kernel = np.ones((10, 10), np.uint8)
            frame_mask = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, kernel)
#            frame_mask = cv2.erode(frame_mask, kernel, iterations=2)
            
            cv2.imshow(self.windows["camera"], frame)
            cv2.imshow(self.windows["hsv"], frame_hsv)
            cv2.imshow(self.windows["mask"], frame_mask)

            key = cv2.waitKey(1) & 0xff
            if key == self.keys["quit"]:
                break

if __name__ == '__main__':
    app = App()
    app.run()

