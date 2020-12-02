import cv2
import time
import pandas
from datetime import datetime

statusList=[None, None]
timeList=[]
df=pandas.DataFrame(columns=["Start", "End"])
firstFrame=None
video=cv2.VideoCapture(0)

while True:
    check, frame=video.read()
    status=0
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if firstFrame is None:
        firstFrame=gray
        continue
    
    delta=cv2.absdiff(firstFrame, gray)
    thresh=cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]
    #thresh looks at the delta between first frame's numpy array and current frames numpy arrays and assigns white to any difference found greater than 30.
    thresh=cv2.dilate(thresh, None, iterations=2) 

    (cnts,_) =cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for i in cnts:
        if cv2.contourArea(i) < 5000:
            continue
        status=1
        (x, y, w, h) =cv2.boundingRect(i)
        #x, y, w, h get assigned automatically based on i
        cv2.rectangle(frame, (x, y), (x+w, x+y), (0, 255, 0), 3)

    statusList.append(status)
    statusList=statusList[-2:]
    #This lists out only the last 2 items in the list, meant to help by limiting memory usage. If script is running for hours at a time.
    if statusList[-1]==1 and statusList[-2]==0:
        timeList.append(datetime.now())
    if statusList[-1]==0 and statusList[-2]==1:
        timeList.append(datetime.now())
    
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta)
    cv2.imshow("Threshold Frame", thresh)
    cv2.imshow("Color Frame", frame)
     
    key=cv2.waitKey(1)

    if key == ord('q'):
        if status==1:
            timeList.append(datetime.now())
        break
    #Press q on keyboard to close script
    
print(statusList)
print(timeList)

for i in range(0,len(timeList),2):
    df=df.append({"Start":timeList[i], "End":timeList[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()