# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 22:19:02 2020

@author: nagaraj
"""

import numpy as np
import matplotlib.pyplot as plt
import math  

from scipy.spatial.distance import cosine
import cv2

cam = cv2.VideoCapture(0)

# Create some random colors
color = np.random.randint(0,255,(100,3))

# Take first frame and find corners in it
ret, old_frame = cam.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
#p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Create a mask image for drawing purposes
mask = np.zeros_like(old_frame)
mask_features = np.zeros_like(old_gray)
mask_features[:,0:20] = 1
mask_features[:,620:640] = 1

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 3,
                       blockSize = 7,
                       mask = mask_features)

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def init_new_features(gray_frame):
    corners = cv2.goodFeaturesToTrack(gray_frame, **feature_params)
    return corners

def calculateDistance(x1,y1,x2,y2):  
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
    return dist  

corners = init_new_features(old_gray)

while True:
    try:
        cam_moved = False
        cam_status = None
        ret,frame = cam.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, corners, None, **lk_params)
        
        good_new = p1
        good_old = corners
        
        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            
            distance = calculateDistance(a,b,c,d)
         
            if distance>8:
                cam_moved = True
                # update the previous frame and previous points
                old_gray = frame_gray.copy()
                corners = init_new_features(old_gray)
            else:
                old_gray = frame_gray.copy()
                corners = good_new.reshape(-1,1,2)
                
            mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        
        if cam_moved is True:
            it = np.random.rand(1)[0]
            print('Camera moved '+ str(it))
            cam_status = 'Camera moved'
            cv2.putText(frame, cam_status, (20, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        img = cv2.add(frame,mask)
        
        cv2.imshow('frame',img)
        
        mask = np.zeros_like(old_frame)
        if corners is None:
            corners = init_new_features(old_gray)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            cam.release()
        
    except TypeError as e:
        print(e)
        break
