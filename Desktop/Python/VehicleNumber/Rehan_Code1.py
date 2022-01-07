import cv2
# Import libraries
import numpy
import cv2
import datetime

#VEHICLE AND PLATE DETECTION
cap = cv2.VideoCapture('Traffic.mp4')
car_cascade = cv2.CascadeClassifier('cars.xml')
while True:
    ret, frames = cap.read()
    
    if ret:
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        dt = str(datetime.datetime.now())
        frames = cv2.putText(frames, dt,
                            (10, 100),
                            font, 0.8,
                            (255, 255, 255),
                            4, cv2.LINE_8)
        
        
    
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
   
    cars = car_cascade.detectMultiScale(gray, 1.1, 1)
    
   
    for (x,y,w,h) in cars:
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
  
    cv2.imshow('video2', frames)
    
    if cv2.waitKey(33) == 27:
        break

cv2.destroyAllWindows()
# Process until end.

