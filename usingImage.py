import cv2
import pytesseract
import numpy as np
import os
#############################################
width, height = 120, 50
newSize = (60, 25)
nPlateCascade = cv2.CascadeClassifier("Resource/haarcascade_russian_plate_number.xml")
minArea = 200
color = (81, 57, 33)
color1 = (106, 129, 207)
###############################################
path = 'Resource/p2.jpg'
name = path.split('/')
name = name[1]
img = cv2.imread(path)
cv2.imshow('Car image', img)
img = cv2.resize(img,(640, 480))
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgCanny = cv2.Canny(imgBlur, 200, 200)
    kernel = np.ones((3, 3))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres

def getContours(img):
    contours, Hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxArea = 0
    biggest = np.array([])
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 150:
            cv2.drawContours(imgContours, cnt, -1, color, 2)  # contour index = -1: draw all the contours
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            if len(approx) == 4 and area > maxArea:
                maxArea = area
                biggest = approx

        cv2.drawContours(imgContours, biggest, -1, color1, 5)  # contour index = -1: draw all the contours
    return biggest

def reoder(biggest):
    biggest = biggest.reshape((4, 2))
    newPoints = np.zeros((4, 2), np.int32)
    add = biggest.sum(axis=1)
    newPoints[0] = biggest[np.argmin(add)]
    newPoints[2] = biggest[np.argmax(add)]
    diff = np.diff(biggest, 1)
    newPoints[1] = biggest[np.argmin(diff)]
    newPoints[3] = biggest[np.argmax(diff)]
    return newPoints

def wrap(img, biggest):
    if biggest.size != 0:
        biggest = reoder(biggest)
        points1 = np.float32(biggest)
        points2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        matrix = cv2.getPerspectiveTransform(points1, points2)
        imgWrap = cv2.warpPerspective(img, matrix, (width, height))
        # imgWrap = imgWrap[2:imgWrap.shape[0] - 2, 2:imgWrap.shape[1] - 2]
    else:
        imgWrap = img
    return imgWrap

for (x, y, w, h) in numberPlates:
    area = w * h
    if area > minArea:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        imgRoi = img[y:y + h, x:x + w]
        imgRoi = cv2.resize(imgRoi, (width, height))
        imgContours = imgRoi.copy()
        imgThres = preProcessing(imgRoi)
        biggest = getContours(imgThres)
        imgWrap = wrap(imgRoi, biggest)
        imgWrap = cv2.resize(imgWrap, (width, height))

        path = os.path.join('Resource/Scanned', name)
        if os.path.exists(path) == False:
            cv2.imwrite(path, imgWrap)

        imgStack = stackImages(2, ([imgThres], [imgContours], [imgWrap]))
        cv2.imshow("Work flow", imgStack)
        cv2.imwrite('workflow.jpg', imgStack)
        cv2.waitKey(50000)

