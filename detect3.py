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

#greenLower = (50, 00, 50)
#greenUpper = (230, 200, 255)

greenLower = (40, 20, 50)
greenUpper = (255, 255, 255)


pts = {}
dict_center = {}
dict_radius = {}
temp = 0
for i in range(0,300):
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
    radius = {}
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        # find all contour instead
        for i in range(0,len(cnts)):
            c[i] = cnts[i]
            ((x, y), radius[i]) = cv2.minEnclosingCircle(c[i])
            M = cv2.moments(c[i])
            center[i] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            
            cv2.circle(frame, (int(x), int(y)), int(radius[i]),(0, 255, 255), 2)
            cv2.circle(frame, center[i], 5, (0, 0, 255), -1)
    dict_center[temp] = center.copy()
    dict_radius[temp] = radius.copy()
    try:
        for i in range(0, len(dict_center[temp-1])):
            dist[i] = {}
            for k in dict_center[temp]:
                dist[i][k] = distance(dict_center[temp-1][i], dict_center[temp][k])
            match[i] = min(dist[i].iteritems(), key=operator.itemgetter(1))[0]
            cv2.line(frame, dict_center[temp-1][i], dict_center[temp][match[i]], (0, 0, 255),5)
    except:
        whatever = 1

#mycode
#video.write(frame)
# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
    temp +=1

# cleanup the camera and close any open windows
camera.release()
video.release()
cv2.destroyAllWindows()
