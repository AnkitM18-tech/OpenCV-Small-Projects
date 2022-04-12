import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

with open("./QRs/datFile.txt") as f:
    dataList = f.read().splitlines()
# print(dataList)

while True:
    success,img = cap.read()
    for barcode in decode(img):
        # print(barcode.data)
        qrData = barcode.data.decode("utf-8")
        if qrData in dataList:
            output = "Authorized"
            color = (0,255,0)
        else:
            output = "Unauthorized"
            color = (0,0,255)
        pts = np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)
        pts2 = barcode.rect
        cv2.putText(img,output,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,color,2)
    cv2.imshow("QR Detected Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break