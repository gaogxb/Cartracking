# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
#args['buffer'] =64

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (100, 66, 6)
#greenUpper = (200, 255, 255)

greenLower = (30, 30, 30)
greenUpper = (255, 255, 255)
pts = {}
for i in range(0,100):
    pts[i] = deque(maxlen=64)


camera = cv2.VideoCapture("IMG_1254.m4v")


fps = camera.get(cv2.CAP_PROP_FPS)

print fps
fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
video = cv2.VideoWriter('output.avi',fourcc, fps, (1920,1080),1)




# keep looping


while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# construct a mask for the color "green", then perform
# a series of dilations and erosions to remove any small
# blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    #initialize parameters, saving in dictionary
    center = {}
    c = {}
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        # find all contour instead
        for i in range(0,len(cnts)):
            c[i] = cnts[i]
            ((x, y), radius) = cv2.minEnclosingCircle(c[i])
            M = cv2.moments(c[i])
            center[i] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size

            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center[i], 5, (0, 0, 255), -1)

    # update the points queue
    for k in range(0,len(cnts)):
        try:
            pts[k].appendleft(center[k])
        except:
            print(k)
            print(len(cnts))
        # loop over the set of tracked points
        for i in xrange(1, len(pts[k])):
            # if either of the tracked points are None, ignore
            # them
            if pts[k][i - 1] is None or pts[k][i] is None:
                continue
        
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)#argsbuffer=64
            if np.abs(pts[k][i][0] - pts[k][i - 1][0]) <30:
                cv2.line(frame, pts[k][i - 1], pts[k][i], (0, 0, 255),5)
        #mycode
#video.write(frame)
# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# cleanup the camera and close any open windows
camera.release()
video.release()
cv2.destroyAllWindows()
