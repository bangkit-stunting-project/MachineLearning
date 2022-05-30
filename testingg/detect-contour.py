import cv2 as cv 
import numpy as np
import random as rand

def tresh_calback(val) :
    threshold = val

    canny_outuput = cv.Canny(gray_img, threshold, threshold*2)

    _, contour = cv.findContours(canny_outuput, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    contour_poly = [None]*len(contour)
    boundRect = [None]*len(contour)
    center = [None]*len(contour)
    radius = [None]*len(contour)

    for i, c in enumerate(contour) :
        contour_poly[i] = cv.approxPolyDP(c, 3, True)
        boundRect[i] = cv.boundingRect(contour_poly[i])
        center[i], radius[i] = cv.minEnclosingCircle(contour_poly[i])

    drawing = np.zeros((canny_outuput.shape[0], canny_outuput.shape[1], 3), dtype=np.uint8)

    for i in range(len(contour)): 
        color = (rand.randint(0,256), rand.randint(0,256), rand.randint(0,256))
        cv.drawContour(drawing, contour_poly, i, color)
        cv.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
        cv.circle(drawing, (int(center[i][0])), int(center[i][1]), int(radius[i]), color, 2)


img = cv.imread('../dataset/image-dataset/dataset-makanan-ibu/Ayam Taliwang/08fb237c8c.jpg')
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

source_window = 'Source'
cv.namedWindow(source_window)
cv.imshow(source_window, img)
# cv.waitkey(0)

max_tresh=255
tresh =100
cv.createTrackbar('Canny Tresh:', source_window, tresh, max_tresh, tresh_calback)