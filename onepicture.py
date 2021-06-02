import time

import cv2 as cv
import numpy as np
import argparse
#load the tonsorflow model *weights
net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
#SETINGS THAT DURING THE TRAINIG WAS PERFORMED
inWidth = 368
inHeight = 368
thr=0.2

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]


#img = cv.imread('SIT7.jfif')
#img = cv.imread('body2.png')
#img = cv.imread('sit8.jfif')
#img = cv.imread('sit10.jfif')
#img = cv.imread('sit&&.jfif')
#img = cv.imread('sit9.jfif')
#img = cv.imread('sit12.jfif')
#img = cv.imread('sit6.jfif')
#img = cv.imread('sit5.jfif')
#img = cv.imread('sit4.jfif')
#img = cv.imread('sit3.jfif') notworking
#img = cv.imread('sit2.jfif')
img = cv.imread('body.jfif')
#img = cv.imread('sleeping3.jfif')

img=cv.resize(img,(450,650))

#cv.imshow('RECT',img)
#cap = cv.VideoCapture(0)


frameWidth = img.shape[1]
frameHeight = img.shape[0]
net.setInput(cv.dnn.blobFromImage(img, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
#cv.dnn.blobFromImage to grab the image
#1.0 SCALE
# 255/2=127.5

out = net.forward()
out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

assert (len(BODY_PARTS) == out.shape[1])
    #LIST OF POINTS OF THE BODY-----------------------------------------------------------------------------
points = []
for i in range(len(BODY_PARTS)):# 18part
        # Slice heatmap of corresponging body's part.
    heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way
        # _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result, None)
    _, conf, _, point = cv.minMaxLoc(heatMap)
    x = (frameWidth * point[0]) / out.shape[3]
    y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
    points.append((int(x), int(y)) if conf > thr else None)
#patterns-----------------------------------------------------------------------------

for pair in POSE_PAIRS:
    partFrom = pair[0]
    partTo = pair[1]
    assert (partFrom in BODY_PARTS)
    assert (partTo in BODY_PARTS)

    idFrom = BODY_PARTS[partFrom]
    idTo = BODY_PARTS[partTo]

    if points[idFrom] and points[idTo]:
        cv.line(img, points[idFrom], points[idTo], (0, 255, 0), 3)
        #cv.ellipse(img, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
        #cv.ellipse(img, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

#t, _ = net.getPerfProfile()
#freq = cv.getTickFrequency() / 1000
# TRAITEMENT OF THE POSE----------------------------------------------------------


cv.ellipse(img, points[1], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)  #HEART | neck
cv.ellipse(img, points[12], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED) #FOOT
cv.ellipse(img, points[9], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED) #FOOT
cv.ellipse(img, points[8], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED) #RHIP MIDDLE
cv.ellipse(img, points[11], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED) #LHIP MIDDLE
heart=points[1]
rhip=points[8]
lhip=points[11]
lknee=points[12]
rknee=points[9]
#print("left {}".format(lknee))
#print("right {}".format(rknee))


#test in the heart point ---------
infoExist=True

if(heart is not None ):
    print("heart exists")
    if (lhip is not None and rhip is not None):
        XroundHip = abs((lhip[0] + rhip[0]) / 2)
        YroundHip = abs((lhip[1] + rhip[1]) / 2)

        widthHip = abs((((( rhip[0]- lhip[0] )**2) + ((rhip[1]-lhip[1])**2) )**0.5))

    elif (lhip is None and rhip is not None):
        XroundHip = abs(rhip[0])
        YroundHip = abs(rhip[1])
        distance = (((( rhip[0]- heart[0] )**2) + ((rhip[1]-heart[1])**2) )**0.5)
        widthHip = abs(distance/2)

    elif (lhip is not None and rhip is None):
        XroundHip = abs(lhip[0])
        YroundHip = abs(lhip[1])
        distance = ((((lhip[0] - heart[0]) ** 2) + ((lhip[1] - heart[1]) ** 2)) ** 0.5)
        widthHip = abs(distance / 2)
    else:
        infoExist = False

else:
    infoExist=False

#HEART
#widthHip=abs(lhip[0]-rhip[0])
#XmiddleHip=abs((lhip[0]+rhip[0])/2)
#YmiddleHip=abs((lhip[1]+rhip[1])/2)

if(infoExist):
    XsupHeart = XroundHip + widthHip
    XinfHeart = XroundHip - widthHip

    # TEST OF SITTING
    Ldx = abs(XroundHip - heart[0])
    Ldy = abs(YroundHip - heart[1])
    if (Ldx > Ldy):
        cv.putText(img, 'slepping', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
    else:
        # KNEE of the sitting
        if (lknee is not None and rknee is not None):
            XroundKnee = abs((lknee[0] + rknee[0]) / 2)
            YroundKnee = abs((lknee[1] + rknee[1]) / 2)
        elif (lknee is None and rknee is not None):
            XroundKnee = abs(rknee[0])
            YroundKnee = abs(rknee[1])
        elif (lknee is not None and rknee is None):
            XroundKnee = abs(lknee[0])
            YroundKnee = abs(lknee[1])
        else:
            infoExist= False
        if(infoExist):
            Mdx = abs(XroundHip - XroundKnee)
            Mdy = abs(YroundHip - YroundKnee)
            YsupKnee = YroundHip + widthHip
            YinfKnee = YroundHip - widthHip
            if (Mdx>Mdy or (YroundKnee > YinfKnee and YroundKnee < YsupKnee)):
                # Draw background rectangle
                cv.rectangle(img, (0, 0), ( 80, 25), (208,224,64), -1)
                cv.putText(img, 'SITTING', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
            else :
                cv.rectangle(img, (0, 0), ( 80, 25), (208,224,64), -1)
                cv.putText(img, 'standing', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))


        else:
            cv.putText(img, 'moving', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
else:
    cv.putText(img, 'WARNING', (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))



#------------------------------------------------------------------------------------
#estimated_image=img
cv.imshow('estimated',img)
cv.waitKey(0)
cv.destroyAllWindows()