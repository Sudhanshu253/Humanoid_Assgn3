import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Cheating video 
cap = cv2.VideoCapture(r"/Users/sudhanshu/Desktop/ML/Python/env/Assignment3_231045/Cheat.mp4")
#plz comment out for no cheat video
#cap = cv2.VideoCapture(r"/Users/sudhanshu/Desktop/ML/Python/env/Assignment3_231045/No_cheat.mp4")

# Function to detect bottle using color masking
def detect_bottle(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Define range for purple color
    lower_purple = np.array([125, 50, 50])
    upper_purple = np.array([150, 255, 255])
    mask = cv2.inRange(hsv_frame, lower_purple, upper_purple)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour, which should be the bottle
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        top_left = (x, y)
        bottom_right = (x + w, y + h)
        return top_left, bottom_right
    else:
        return None, None

# Function to simulate bottle flipping
def simulate_flip(frame, top_left, bottom_right):
    if top_left and bottom_right:
        # Draw the bottle (rectangle for simplicity)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
    return frame

# Function to check if hand landmarks intersect with the bottle
def check_intersection(hand_landmarks, top_left, bottom_right):
    if not top_left or not bottom_right:
        return False
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
        if top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]:
            return True
    return False

# Initialize state variables
initial_hands_away = False
flipping_started = False

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame color to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        # Detect the bottle using color masking
        top_left, bottom_right = detect_bottle(frame)
        
        # Simulate the bottle flip
        frame = simulate_flip(frame, top_left, bottom_right)
        
        cheating_detected = False
        
        # Check for hand intersections with the bottle
        if result.multi_hand_landmarks:
            hands_near_bottle = False
            for hand_landmarks in result.multi_hand_landmarks:
                if check_intersection(hand_landmarks, top_left, bottom_right):
                    hands_near_bottle = True
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if not hands_near_bottle:
                # If hands are detected away from the bottle with high confidence
                initial_hands_away = True
            
            if initial_hands_away and hands_near_bottle:
                # Detect cheating after the initial hands are away
                cheating_detected = True
        
        # Display cheating message if detected
        if cheating_detected:
            cv2.putText(frame, "Cheating!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the result
        cv2.imshow('Bottle Flipping Game', frame)
        
        if cv2.waitKey(25) & 0xFF == 27:  # Press 'Esc' to exit
            break

cap.release()
cv2.destroyAllWindows()
