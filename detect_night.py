# import the necessary packages
from collections import deque
import operator
import numpy as np
import argparse
import imutils
import cv2
from math import atan2, degrees, pi

class car:
    center = []
    speed = []
    angle = []
    frame = []
    count = 0
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

#correct for some cars
#greenLower = (35, 30, 90)
#greenUpper = (250, 250, 205)


greenLower = (30, 30, 40)
greenUpper = (250, 250, 205)

pts = {}
dict_center = {}
dict_radius = {}
dict_car = {}
dist = {}
match = {}
temp = 0

for i in range(0,300):
    pts[i] = deque(maxlen=64)

camera = cv2.VideoCapture("road.mp4")
fgbg = cv2.createBackgroundSubtractorMOG2()

fps = camera.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
video = cv2.VideoWriter('track_assignment.avi',fourcc, fps, (400,225),1)




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
    #frame = imutils.resize(frame, width=600)
    #frame = imutils.resize(frame, width=400)
    fgmask = fgbg.apply(frame)
    (thresh, im_bw) = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #frame = fgmask
# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = im_bw
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
            if radius[i] >200:
                cv2.circle(frame, (int(x), int(y)), int(radius[i]),(0, 255, 255), 2)
                cv2.circle(frame, center[i], 5, (0, 0, 255), -1)
    dict_center[temp] = center.copy()
    dict_radius[temp] = radius.copy()
    #loop from 2, avoid error
    if temp>20:
        #loop for every frame
        for i in range(0, len(dict_center[temp-1])):
            #loop for every center
            
            dist[i] = {}
            for k in dict_center[temp]:
                dist[i][k] = distance(dict_center[temp-1][i], dict_center[temp][k])
            match[i] = min(dist[i].iteritems(), key=operator.itemgetter(1))[0]
            if distance(dict_center[temp-1][i], dict_center[temp][match[i]]) <20:
                myangle = angle(dict_center[temp-1][i], dict_center[temp][match[i]])
                if True:
                    #(myangle >70 and myangle < 110) or ((myangle>250) and (myangle<290)):
                    if (distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034 > 2:
                        #if ((dict_radius[temp-1][i] / dict_radius[temp][match[i]])>0.85 and (dict_radius[temp-1][i] / dict_radius[temp][match[i]])<1.15):
                        if 0:
                            #and (dict_radius[temp-1][i]>10) and (dict_radius[temp][match[i]]>10):
                            cv2.line(frame, dict_center[temp-1][i], dict_center[temp][match[i]], (0, 0, 255),5)
                            #now we have a new center:dict_center[temp][match[i]] which connected to dict_center[temp-1][i]
                            if len(dict_car) == 0:
                                dict_car[0] = {}
                                dict_car[0]['center'] = []
                                dict_car[0]['speed'] = []
                                dict_car[0]['angle'] = []
                                dict_car[0]['frame'] = []
                                dict_car[0]['center'].append(dict_center[temp][match[i]])
                                dict_car[0]['speed'].append((distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                dict_car[0]['angle'].append((angle(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                dict_car[0]['frame'].append(temp)
                                dict_car[0]['count'] = 1
                            else:
                                found = 0
                                for m in dict_car:
                                    for j in range(0,dict_car[m]['count']):
                                        if (distance(dict_center[temp][match[i]], dict_car[m]['center'][j]) < 50) and (np.abs(temp - dict_car[m]['frame'][j])<2):
                                            dict_car[m]['center'].append(dict_center[temp][match[i]])
                                            dict_car[m]['speed'].append((distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                            dict_car[m]['angle'].append((angle(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                            dict_car[m]['frame'].append(temp)
                                            dict_car[m]['count'] +=1
                                            found = 1
                                            #print dict_center[temp][match[i]]
                                            #print dict_car[m]['center'][j]
                                            #print temp
                                            #print dict_car[m]['frame'][j]
                                            #print m
                                            break
                                if found ==0:
                                    current_len = len(dict_car)
                                    #create new car
                                    dict_car[current_len] = {}
                                    dict_car[current_len]['center'] = []
                                    dict_car[current_len]['speed'] = []
                                    dict_car[current_len]['angle'] = []
                                    dict_car[current_len]['frame'] = []
                                    dict_car[current_len]['count'] = 0
                                    #add features
                                    dict_car[current_len]['center'].append(dict_center[temp][match[i]])
                                    dict_car[current_len]['speed'].append((distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                    dict_car[current_len]['angle'].append((angle(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
                                    dict_car[current_len]['frame'].append(temp)
                                    dict_car[current_len]['count'] +=1
    #print ("center: ") + str(dict_center[temp][match[i]])
#print ("speed: ") + str((distance(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
#print ("angle: ") + str((angle(dict_center[temp-1][i], dict_center[temp][match[i]])*fps)*0.034)
#print ("frame: ") + str(temp)

#mycode

# show the frame to our screen
    frame = imutils.resize(frame, width=400)
    mask = imutils.resize(mask, width=400)
#print (frame.shape)
#cv2.imshow("Frame", frame)
    video.write(frame)
    key = cv2.waitKey(1) & 0xFF
    
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
temp +=1

# cleanup the camera and close any open windows
camera.release()
video.release()
cv2.destroyAllWindows()
