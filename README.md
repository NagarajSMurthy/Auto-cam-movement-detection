# Auto-cam-movement-detection

Background subtraction is the basis for many computer vision tasks like motion detection, Invisibility cloak, etc. . It is a simple concept which comes with a drawback. Background subtraction works only with static background images/frames, that means, if you change the position of your camera it'll fail or gives very bad results. One possible way to overcome this is to initialize the background frame to a new static frame whenever a motion in the camera is detected. 

Detecting the movement of the camera automatically is not a simple task for obvious reasons. Here, I have made an atempt to detect the movement of the camera either external or inbuilt using the concept of optical flow. 

![](camera_movement.gif)

Steps:
1. The features are selected using the ShiTomasi corner detection (http://www.ai.mit.edu/courses/6.891/handouts/shi94good.pdf). These features are selected only in the border regions assuming that the foreground object very rarely occupies the border region, in other words, the border region gives features belonging to the background region. 
2. These feature points are given to the Lucas-Kanade optical flow to track the points.
3. If the distance between the previous and the current tracked points exceeds a threshold value, it can be concluded that the camera itself has been moved otherwise not.

This can be combined with other computer vision applications for better results, however this may not be the most robust solution for detecting camera movement. 


