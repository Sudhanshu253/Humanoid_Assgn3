import cv2
import numpy as np

# Function to find the center of a contour
def get_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return cX, cY
    else:
        return None

# Open the video file
cap = cv2.VideoCapture('/Users/sudhanshu/Desktop/ML/Python/env/Assignment3_231045/ArcheryB.mp4')

# Variable to store the center of the archery board
archery_board_center = None

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges for sky blue, yellow, and red
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # Create masks for each color
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Combine the red masks
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    
    # Combine all masks
    combined_mask = cv2.bitwise_or(mask_blue, cv2.bitwise_or(mask_yellow, mask_red))
    
    # Find contours in the combined mask
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour which should correspond to the archery board
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        archery_board_center = get_contour_center(largest_contour)
        if archery_board_center:
            # Draw the contour and its center
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, archery_board_center, 5, (0, 0, 255), -1)
    
    # Check if the "shoot" key is pressed
    key = cv2.waitKey(25) & 0xFF
    if key == ord('s') and archery_board_center:
        # Draw a green circle at the center of the archery board
        cv2.circle(frame, archery_board_center, 20, (0, 255, 0), 3)
    
    # Display the result
    cv2.imshow('Detected Archery Board', frame)
    
    # Exit the loop if 'q' is pressed
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
