import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time

# define a video capture object
vid = cv2.VideoCapture(1)

#initalize mqtt 
broker_address = ("10.243.28.115")
client = mqtt.Client("Kelli")
client.connect(broker_address)

while(True):
    ret, frame = vid.read()
    cv2.imshow('frame', frame)
    cv2_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    b,g,r = cv2.split(cv2_frame)
    #(b,g) gives red, (r,g) gives blue.. check switching color order
    red = cv2.subtract(b,g)
    cv2.imshow('red', red)
    blurred = cv2.GaussianBlur(red, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.
                            CHAIN_APPROX_SIMPLE)
    cv2.imshow('thresh', thresh)
    info = []
    for c in cnts[0]:
        # compute the center of the contour
        M = cv2.moments(c)
        area = cv2.contourArea(c)
        #if have more than one red object for right now just have 1 so don't need
        #areas = [row[0] for row in info]
        #order = np.flip(np.argsort(areas))
        #area = info(order[0])
        if area > 35:
            if M["m00"] != 0:
                cX = int(M['m10']/M['m00'])
                cY = int(M['m01']/M['m00'])
                client.publish("ME035", str(cX))
                #print(cX)
            else:
                cX, cY = 0,0
            info.append([area, cX, cY])
            #print(info[0])
            cv2.drawContours(cv2_frame, [c], -1, (0, 255, 0), thickness=cv2.FILLED)
            cv2.circle(cv2_frame, (cX, cY), 7, (255, 0, 0), -1)
            cv2.putText(cv2_frame, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
client.disconnect()
