# import the necessary packages
from collections import deque
import operator
import numpy as np
import argparse
import imutils
import cv2
from math import atan2, degrees, pi

def distance((x1,y1),(x2,y2)):
    return np.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

def angle((x1,y1),(x2,y2)):
    dx = x2 - x1
    dy = y2 - y1
    rads = atan2(dy,dx)
    rads %= 2*pi
    degs = degrees(rads)
    return degs

# construct the argument parse and parse the arguments
#args['buffer'] =64

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (100, 66, 6)
#greenUpper = (200, 255, 255)

greenLower = (30, 30, 30)
greenUpper = (250, 250, 250)
pts = {}
dict_center = {}
dict_radius = {}
dist = {}
match = {}
temp = 0
for i in range(0,300):
    pts[i] = deque(maxlen=64)


camera = cv2.VideoCapture("IMG_1275.m4v")
fgbg = cv2.createBackgroundSubtractorMOG2()

fps = camera.get(cv2.CAP_PROP_FPS)

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
    fgmask = fgbg.apply(frame)
#frame = fgmask
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
            
            #cv2.circle(frame, (int(x), int(y)), int(radius[i]),(0, 255, 255), 2)
            #cv2.circle(frame, center[i], 5, (0, 0, 255), -1)
    dict_center[temp] = center.copy()
    dict_radius[temp] = radius.copy()
    #loop from 2, avoid error
    if temp>2:
        #loop for every frame
        for i in range(0, len(dict_center[temp-1])):
            #loop for every center
            
            dist[i] = {}
            for k in dict_center[temp]:
                dist[i][k] = distance(dict_center[temp-1][i], dict_center[temp][k])
            match[i] = min(dist[i].iteritems(), key=operator.itemgetter(1))[0]
            if distance(dict_center[temp-1][i], dict_center[temp][match[i]]) <20:
                myangle = angle(dict_center[temp-1][i], dict_center[temp][match[i]])
                if (myangle >170 and myangle < 190) or ((myangle<10) or (myangle>350)):
                    cv2.line(frame, dict_center[temp-1][i], dict_center[temp][match[i]], (0, 0, 255),5)
                    if (distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034 > 2:
                        if ((dict_radius[temp-1][i] / dict_radius[temp][match[i]])>0.85 and (dict_radius[temp-1][i] / dict_radius[temp][match[i]])<1.15):
                            print ("center: ") + str(dict_center[temp][match[i]])
                            print ("speed: ") + str((distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                            print ("angle: ") + str((angle(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                            print ("frame: ") + str(temp)

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
