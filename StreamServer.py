
import numpy as np
import cv2
import socket
import time
import paho.mqtt.publish as publish


'''
import  mysql.connector
mydb=mysql.connector.connect(
    host='192.168.1.:3306',
    user='root',
    password='',
    database='healthtracker',
)


cur=mydb.cursor()
s=" INSERT INTO healthtrackerapp_state (id_patient,status) VALUES (%s, %s) "
b1= ("2","standing")
#CC 1E 0C 30


cur.execute(s,b1)
mydb.commit()
'''
class VideoStreamingTest(object):
    def __init__(self, host, port):

        self.server_socket = socket.socket()
        self.server_socket.bind((host, port))
        self.server_socket.listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.connection = self.connection.makefile('rb')
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.streaming()

    def streaming(self):
        # dnn : deep neural network is the manager system of content
        # Load the model imported from Tensorflow
        net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
        # SETINGS THAT DURING THE TRAINIG WAS PERFORMED
        inWidth = 368
        inHeight = 368
        thr = 0.2

        # the info that we should return
        movement = ""

        BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                      "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                      "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                      "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

        # determinate all the possible combinations between the parts of the body (parts are going to be linked)
        POSE_PAIRS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                      ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                      ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                      ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                      ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]
        # Background subtraction (BS) is a common and widely used technique for generating a foreground mask
        # (namely, a binary image containing the pixels belonging to moving objects in the scene) by using static cameras.
        fgbg = cv2.createBackgroundSubtractorMOG2()
        j = 0
        try:
            '''
            print("Host: ", self.host_name + ' ' + self.host_ip)
            print("Connection from: ", self.client_address)
            print("Streaming...")
            print("Press 'q' to exit")
            '''

            # need bytes here
            stream_bytes = b' '
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    #image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    #cv2.imshow('image', image)

                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    # Convert each frame to gray scale and subtract the background
                    try:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        fgmask = fgbg.apply(gray)

                        # Find contours
                        # image, contours, hierarchy	=	cv.findContours(	image, mode, method[, contours[, hierarchy[, offset]]]	)
                        # RETR_TREE: 	retrieves all of the contours and reconstructs a full hierarchy of nested contours with order.
                        # CHAIN_APPROX_SIMPLE :compresses horizontal, vertical, and diagonal segments and leaves only their end points.
                        # For example, an up-right rectangular contour is encoded with 4 points.
                        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                        if contours:

                            # List to hold all areas
                            areas = []

                            for contour in contours:
                                # the function computes the a contour area
                                ar = cv2.contourArea(contour)
                                areas.append(ar)

                            max_area = max(areas, default=0)

                            max_area_index = areas.index(max_area)

                            cnt = contours[max_area_index]
                            # Definition of moments in image processing is borrowed from physics.
                            # Assume that each pixel in image has weight that is equal to its intensity.
                            # Then the point you defined is centroid (a.k.a. center of mass) of image.
                            M = cv2.moments(cnt)
                            # The cv2.boundingRect() function of OpenCV is used to draw an approximate rectangle around the binary image.
                            # This function is used mainly to highlight the region of interest after obtaining contours from an image.
                            # Straight Bounding Rectangle
                            x, y, w, h = cv2.boundingRect(cnt)

                            cv2.drawContours(fgmask, [cnt], 0, (255, 255, 255), 3, maxLevel=0)

                            # the first video in black and white
                            cv2.imshow('FGMASK', fgmask)

                            if h < w:
                                j += 1
                                print(j)
                                if j > 5:
                                    print("sending 1")
                                    publish.single("alarme", "1", hostname="192.168.1.100")
                                    cv2.rectangle(frame, (0, 0), (140, 25), (208, 224, 64), -1)
                                    cv2.putText(frame, 'falling', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
                                    movement = "falling"
                                    print("--------------------------------------------------")
                                    print(movement)

                            if h > w:
                                j = 0

                        #####################################################################################################
                        frameWidth = frame.shape[1]
                        frameHeight = frame.shape[0]
                        # [blobFromImage] creates 4-dimensional blob from image.
                        # Optionally resizes and crops image from center, subtract mean values,
                        # scales values by scalefactor, swap Blue and Red channels.
                        # retval = cv.dnn.blobFromImage(image[, scalefactor[, size[, mean[, swapRB[, crop[, ddepth]]]]]]    )
                        net.setInput(
                            cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True,
                                                  crop=False))
                        # 1.0 SCALE
                        # 255/2=127.5

                        out = net.forward()
                        out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

                        # assert (len(BODY_PARTS) == out.shape[1])
                        # LIST OF POINTS OF THE BODY-----------------------------------------------------------------------------
                        points = []
                        for i in range(len(BODY_PARTS)):  # 18part
                            # Slice heatmap of corresponging body's part.
                            heatMap = out[0, i, :, :]

                            # Originally, we try to find all the local maximums. To simplify a sample
                            # we just find a global one. However only a single pose at the same time
                            # could be detected this way.
                            _, conf, _, point = cv2.minMaxLoc(heatMap)
                            x = (frameWidth * point[0]) / out.shape[3]
                            y = (frameHeight * point[1]) / out.shape[2]
                            # Add a point if it's confidence is higher than threshold = 0.2.
                            points.append((int(x), int(y)) if conf > thr else None)
                        # patterns-----------------------------------------------------------------------------

                        for pair in POSE_PAIRS:
                            partFrom = pair[0]
                            partTo = pair[1]
                            assert (partFrom in BODY_PARTS)
                            assert (partTo in BODY_PARTS)

                            idFrom = BODY_PARTS[partFrom]
                            idTo = BODY_PARTS[partTo]

                            if points[idFrom] and points[idTo]:
                                cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                                cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                                cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                        # TRAITEMENT OF THE POSE----------------------------------------------------------

                        cv2.ellipse(frame, points[1], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)  # HEART
                        cv2.ellipse(frame, points[12], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)  # FOOT
                        cv2.ellipse(frame, points[9], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)  # FOOT
                        cv2.ellipse(frame, points[8], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)  # RHIP MIDDLE
                        cv2.ellipse(frame, points[11], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)  # LHIP MIDDLE
                        heart = points[1]
                        rhip = points[8]
                        lhip = points[11]
                        lknee = points[12]
                        rknee = points[9]

                        # test in the heart point ---------
                        infoExist = True

                        if (heart is not None):
                            #print("heart exists")
                            if (lhip is not None and rhip is not None):
                                XroundHip = abs((lhip[0] + rhip[0]) / 2)
                                YroundHip = abs((lhip[1] + rhip[1]) / 2)

                                widthHip = abs(((((rhip[0] - lhip[0]) ** 2) + ((rhip[1] - lhip[1]) ** 2)) ** 0.5))

                            elif (lhip is None and rhip is not None):
                                XroundHip = abs(rhip[0])
                                YroundHip = abs(rhip[1])
                                distance = ((((rhip[0] - heart[0]) ** 2) + ((rhip[1] - heart[1]) ** 2)) ** 0.5)
                                widthHip = abs(distance / 2)

                            elif (lhip is not None and rhip is None):
                                XroundHip = abs(lhip[0])
                                YroundHip = abs(lhip[1])
                                distance = ((((lhip[0] - heart[0]) ** 2) + ((lhip[1] - heart[1]) ** 2)) ** 0.5)
                                widthHip = abs(distance / 2)
                            else:
                                infoExist = False

                        else:
                            infoExist = False

                        # HEART
                        # widthHip=abs(lhip[0]-rhip[0])
                        # XmiddleHip=abs((lhip[0]+rhip[0])/2)
                        # YmiddleHip=abs((lhip[1]+rhip[1])/2)

                        if (infoExist):
                            XsupHeart = XroundHip + widthHip
                            XinfHeart = XroundHip - widthHip

                            # TEST OF SITTING
                            Ldx = abs(XroundHip - heart[0])
                            Ldy = abs(YroundHip - heart[1])
                            # if (Ldx > Ldy):
                            #   cv2.putText(frame, 'slepping', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                            if (Ldx < Ldy):
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
                                    infoExist = False
                                if (infoExist):
                                    Mdx = abs(XroundHip - XroundKnee)
                                    Mdy = abs(YroundHip - YroundKnee)
                                    YsupKnee = YroundHip + widthHip
                                    YinfKnee = YroundHip - widthHip
                                    if (Mdx > Mdy or (YroundKnee > YinfKnee and YroundKnee < YsupKnee)):
                                        cv2.rectangle(frame, (0, 0), (80, 25), (208, 224, 64), -1)
                                        cv2.putText(frame, 'SITTING', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 0))
                                        movement = "SITTING"

                                    else:
                                        cv2.rectangle(frame, (0, 0), (80, 25), (208, 224, 64), -1)
                                        cv2.putText(frame, 'standing', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                                    (0, 0, 0))
                                        movement = "STANDING"


                                else:
                                    cv2.rectangle(frame, (0, 0), (80, 25), (208, 224, 64), -1)
                                    cv2.putText(frame, 'moving', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
                                    movement = "MOVING"

                        else:
                            movement = "lack of information"
                            #cv2.rectangle(frame, (0, 0), (80, 25), (208, 224, 64), -1)
                            #cv2.putText(frame, 'lack of information', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 0))

                        print(movement)
                        cv2.imshow('video', frame)

                    except Exception as e:
                        break










                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break








        finally:
            self.connection.close()
            self.server_socket.close()













if __name__ == '__main__':
    # host, port
    h, p = "192.168.1.101", 8000
    VideoStreamingTest(h, p)
