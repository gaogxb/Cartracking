import numpy as np
import cv2
import imutils
cap = cv2.VideoCapture('IMG_1254_10s.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
video = cv2.VideoWriter('IMG_1254_10s_small.avi',fourcc, fps, (400,711),1)
while(cap.isOpened()):
    ret, frame = cap.read()
    frame = imutils.resize(frame,width = 400)
    print (frame.shape)
    #fgmask = fgbg.apply(frame)
    #fgmask = cv2.erode(fgmask, None, iterations=2)
    #fgmask = cv2.dilate(fgmask, None, iterations=2)
    #cv2.imshow('frame',fgmask)
    #frame = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2RGB)
    video.write(frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
video.release()
cv2.destroyAllWindows()
