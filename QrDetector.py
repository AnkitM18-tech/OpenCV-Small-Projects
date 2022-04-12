import cv2
import numpy as np
from pyzbar.pyzbar import decode

img1 = cv2.imread("./QRs/1.png")
img2 = cv2.imread("./QRs/2.png")
# img3 = cv2.imread("./QRs/barcode.gif")
code1 = decode(img1)
# code2 = decode(img2)
# code3 = decode(img3)
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
# print(code1)
# print(code2)
# print(code3)
while True:
    success,img = cap.read()
    for barcode in decode(img):
        # print(barcode.data)
        qrData = barcode.data.decode("utf-8")
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.putText(img,qrData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
    cv2.imshow("QR Detected Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break