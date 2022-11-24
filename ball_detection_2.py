import cv2 as cv
import numpy as np
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

#videoCapture = cv.VideoCapture(2)
videoCapture = cv.VideoCapture(args["video"])
prevCircle = None
dist = lambda x1,y1,x2,y2: (x1-x2)**2+(y1-y2)**2

while True:
    ret, frame = videoCapture.read()
    if not ret: break

    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)

    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 2, 1000,
                              param1=100, param2=30, minRadius=1, maxRadius=10)

    if circles is not None:
        print(circles)
        circles = np.uint16(np.around(circles))
        chosen = None
        for circle in circles[0, :]:
            if chosen is None: chosen = circle
            if prevCircle is not None:
                if dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1]) <= dist(circle[0],circle[1],prevCircle[0],prevCircle[1]):
                    chosen = circle
        cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 20)
        cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,255), 20)
        prevCircle = chosen

    cv.imshow('circles', frame)

    if cv.waitKey(1) & 0xFF == ord('q'): break

videoCapture.release()
cv.destroyAllWindows()
