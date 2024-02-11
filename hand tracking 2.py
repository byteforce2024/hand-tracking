import mediapipe as mp
import cv2 
from serial import Serial

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

arduino=Serial("COM7",9600)


while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: 
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 20 :
                    cv2.circle(image, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: 
            sum=0
            # index finger
            finger_tip = handLms.landmark[8]
            tip_y = finger_tip.y

            if tip_y < 0.72:
                sum=sum+1

            #middle finger
            finger_tip = handLms.landmark[12]
            tip_y = finger_tip.y

            if tip_y < 0.72:
                sum=sum+1
            
            #ring finger
            finger_tip = handLms.landmark[16]
            tip_y = finger_tip.y

            if tip_y < 0.72:
                sum=sum+1
            
            # little finger 
            finger_tip = handLms.landmark[20]
            tip_y = finger_tip.y

            if tip_y < 0.72:
                sum=sum+1

            #thumb
            finger_tip = handLms.landmark[4]
            tip_y = finger_tip.y

            
            if tip_y < 0.685:
                sum=sum+1

            #print
            cv2.putText(image, str(sum) , (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            arduino.write(str(sum).encode())

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)

            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Output", image)
    if cv2.waitKey(1)& 0xFF == ord('q') :
        break
cv2.destroyAllWindows()
cap.release()
arduino.close()