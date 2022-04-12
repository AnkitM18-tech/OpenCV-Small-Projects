import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Tesseract-OCR\\tesseract.exe"

# Detecting Characters
img = cv2.imread("./test.png")
img = cv2.resize(img,(1280,960))
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img))
hImg,wImg,_ = img.shape
# conf = r"--oem 3 --psm 6 outputbase digits"
boxes = pytesseract.image_to_boxes(img)
for b in boxes.splitlines():
    b = b.split(" ")
    # print(b)
    x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(img,(x,hImg-y+5),(w,hImg-h-5),(0,0,255),3)
    cv2.putText(img,str(b[0]),(x,hImg-y+30),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

# # Detecting Words
# img = cv2.imread("./test.png")
# img = cv2.resize(img,(1280,960))
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# # print(pytesseract.image_to_string(img))
# hImg,wImg,_ = img.shape
# boxes = pytesseract.image_to_data(img)
# # print(boxes)
# for x,b in enumerate(boxes.splitlines()):
#     if x!= 0:
#         b = b.split()
#         # print(b)
#         if len(b) == 12:
#             x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
#             cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
#             cv2.putText(img,str(b[11]),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

# # Detecting Numbers
# img = cv2.imread("./test.png")
# img = cv2.resize(img,(1280,960))
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
# # print(pytesseract.image_to_string(img))
# hImg,wImg,_ = img.shape
# conf = r"--oem 3 --psm 6 outputbase digits" #backend engine modes
# boxes = pytesseract.image_to_data(img,config=conf)
# # print(boxes)
# for x,b in enumerate(boxes.splitlines()):
#     if x!= 0:
#         b = b.split()
#         # print(b)
#         if len(b) == 12:
#             x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
#             cv2.rectangle(img,(x,y-5),(x+w,y+h+5),(0,0,255),3)
#             cv2.putText(img,str(b[11]),(x,y-10),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

cv2.imshow("Result",img)
cv2.waitKey(0)