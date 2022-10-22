import cv2
import imutils
import math
#pip install playsound
from playsound import playsound
import threading
import time  
# Initializing the HOG person
# detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


flag = 0


def sound_play():
   global flag
   while True:
      while flag:
         playsound('請保持距離.mp3')
         time.sleep(5)
         flag=0


def Image_recognition():
    global flag,dst
    cap = cv2.VideoCapture('vid.mp4')
    
    while cap.isOpened():

        # Reading the video stream
        ret, image = cap.read()
        if ret:
            image = imutils.resize(image,width=min(800, image.shape[1]))
       

            # Detecting all the regions in the 
            # Image that has a pedestrians inside it
            (regions, _) = hog.detectMultiScale(image,winStride=(4, 4),padding=(4, 4),scale=1.05)
            A = [0]*len(regions)

            ##計算人的座標
            for x in range(len(regions)):
                A[x] = (regions[x][0]+int(regions[x][2]/2),regions[x][1]+int(regions[x][3]/2.0))

            for x in range(len(A)):
                for j in range(len(A)):        
                     if x<j:
                         ##算距離
                         
                         dx ,dy = A[x][0] - A[j][0] , A[x][1] - A[j][1]
                         dst = int(math.sqrt(dx**2 + dy**2))
                         ##如果社交距離小於100
                         
                         if dst<100 :
                             cv2.rectangle(image,
                                           (regions[x][0], regions[x][1]),
                                           (regions[x][0] + regions[x][2], regions[x][1] + regions[x][3]), (0, 0, 255), 2)
                             print("距離: ",dst)
                             flag = 1
                             cv2.line(image, A[x] , A[j] , (255, 0, 0), 2)
  
            # Showing the output Image
            cv2.imshow("Image", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):break
        else:break



if __name__ == '__main__':
   
    t1 = threading.Thread(target = sound_play)
    t2 = threading.Thread(target = Image_recognition)
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

    cv2.destroyAllWindows()
