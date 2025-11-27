import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats import landmark_pb2
import time
import random

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

score = 0
x_enemy = random.randint(50, 600)
y_enemy = random.randint(50, 400)

cap = cv2.VideoCapture(0)

FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_COLOR = (255, 255, 255)

def enemy(frame):
    global score, x_enemy, y_enemy

    cv2.circle(frame, (x_enemy, y_enemy), 25, (0, 200, 0), 5)

    text_score = f'Score: {score}'
    cv2.putText(frame, text_score, (480, 30), FONT, 1, FONT_COLOR, 2, cv2.LINE_AA)

with mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        frame = cv2.flip(frame, 1)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(image)
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        imageHeight, imageWidth, _ = image.shape
        
        enemy(image)
        
        if results.multi_hand_landmarks:
            for hand_id, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

                point = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                    point.x, 
                    point.y, 
                    imageWidth, 
                    imageHeight
                )
                
                if pixelCoordinatesLandmark:
                    finger_tip_x = pixelCoordinatesLandmark[0]
                    finger_tip_y = pixelCoordinatesLandmark[1]
                    cv2.circle(image, (finger_tip_x, finger_tip_y), 25, (0, 200, 0), 5)
                    
                    x_hit = x_enemy - 10 <= finger_tip_x <= x_enemy + 10
                    y_hit = y_enemy - 10 <= finger_tip_y <= y_enemy + 10

                    if x_hit and y_hit:
                        score += 1
                        
                        x_enemy = random.randint(50, 600)
                        y_enemy = random.randint(50, 400)
                        
                        cv2.putText(image, "HIT!", (100, 100), FONT, 1, (0, 0, 255), 4, cv2.LINE_AA)

        cv2.imshow('Hand Tracking Game', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()