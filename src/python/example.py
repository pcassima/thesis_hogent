"""
Official example from the Tinker Board wiki.
This example shows how to use the RaspBerry Pi camera on the Tinker Board for facial recognition.
"""

import sys
import os
import cv2

print(cv2.__version__)
cv2.setNumThreads(4)

faceCascade = cv2.CascadeClassifier("/usr/local/share/OpenCV/haarcascades//haarcascade_frontalface_alt.xml")
cap = cv2.VideoCapture(
    "rkcamsrc io-mode=4 isp-mode=2A tuning-xml-path=/etc/cam_iq/IMX219.xml ! video/x-raw,format=NV12,width=640,height=480 ! videoconvert ! appsink")

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
