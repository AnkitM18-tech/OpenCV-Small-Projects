import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
# img = cv2.imread("./text.jpg")
# img = cv2.resize(img,(frameWidth,frameHeight))

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",0,179,empty)
cv2.createTrackbar("HUE Max","HSV",179,179,empty)
cv2.createTrackbar("SAT Min","HSV",0,255,empty)
cv2.createTrackbar("SAT Max","HSV",255,255,empty)
cv2.createTrackbar("VALUE Min","HSV",0,255,empty)
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)

while True:
    _,img = cap.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos("HUE Min","HSV")
    hue_max = cv2.getTrackbarPos("HUE Max","HSV")
    sat_min = cv2.getTrackbarPos("SAT Min","HSV")
    sat_max = cv2.getTrackbarPos("SAT Max","HSV")
    val_min = cv2.getTrackbarPos("VALUE Min","HSV")
    val_max = cv2.getTrackbarPos("VALUE Max","HSV")

    lower = np.array([hue_min,sat_min,val_min])
    upper = np.array([hue_max,sat_max,val_max])

    mask = cv2.inRange(imgHSV,lower,upper)
    result = cv2.bitwise_and(img,img,mask = mask)
    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img,result])

    # cv2.imshow("Original Image",img)
    # cv2.imshow("HSV Color Space",imgHSV)
    # cv2.imshow("Mask",mask)
    # cv2.imshow("Masked Image",result)
    cv2.imshow("Stacked Image",hStack)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break