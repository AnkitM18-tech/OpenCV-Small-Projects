import cv2
import numpy as np
import Utils

webCamFeed = False
pathImage = "./1.png"
cap = cv2.VideoCapture(0)
cap.set(10,160)
imgHeight = 640
imgWidth = 480

Utils.initializeTrackbars()
count = 0

while True:
    # Blank Image
    imgBlank = np.zeros((imgHeight,imgWidth,3),np.uint8) # Blank Image for Testing
    if webCamFeed:
        success,img = cap.read()
    else:
        img = cv2.imread(pathImage)
        img = cv2.resize(img,(imgWidth,imgHeight)) #Resize Image
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # convert image to grayscale
        imgBlur = cv2.GaussianBlur(imgGray,(5,5),1) # Add Gaussian Blur
        threshold = Utils.valTrackbars() #trackbar values for threshold
        imgThreshold = cv2.Canny(imgBlur,threshold[0],threshold[1]) # apply canny blur
        kernel = np.ones((5,5))
        imgDil = cv2.dilate(imgThreshold,kernel,iterations=2) # apply Dilation
        imgThreshold = cv2.erode(imgDil,kernel,iterations=1) # apply erosion

        # Find All Contours
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS

        # FIND THE BIGGEST COUNTOUR
        biggest, maxArea = Utils.biggestContour(contours) # FIND THE BIGGEST CONTOUR
        if biggest.size != 0:
            biggest=Utils.reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
            imgBigContour = Utils.drawRectangle(imgBigContour,biggest,2)
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[imgWidth, 0], [0, imgHeight],[imgWidth, imgHeight]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))
    
            #REMOVE 20 PIXELS FORM EACH SIDE
            imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(imgWidth,imgHeight))
    
            # APPLY ADAPTIVE THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
    
            # Image Array for Display
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
    
        else:
            imageArray = ([img,imgGray,imgThreshold,imgContours],
                        [imgBlank, imgBlank, imgBlank, imgBlank])
    
        # LABELS FOR DISPLAY
        labels = [["Original","Gray","Threshold","Contours"],
                ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
    
        stackedImage = Utils.stackImages(imageArray,0.75,labels)
        cv2.imshow("Result",stackedImage)
    
        # SAVE IMAGE WHEN 's' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite("./Scanned/myImage"+str(count)+".jpg",imgWarpColored)
            cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                        (1100, 350), (0, 255, 0), cv2.FILLED)
            cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow('Result', stackedImage)
            count += 1
            cv2.waitKey(300)