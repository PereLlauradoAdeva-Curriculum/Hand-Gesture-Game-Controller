import cv2
import numpy as np

# Start video capture from the default webcam
cap = cv2.VideoCapture(0)
direccio = None

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally (mirror view)
    frame = cv2.flip(frame, 1)

    # Convert frame to YCrCb color space (better for skin detection)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

    # Skin color range (adjustable depending on lighting/skin tone)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)

    # Reduce noise using erosion and dilation
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours in the skin mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get the largest contour (assumed to be the hand)
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 1000:
            # Draw the contour on the original frame
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

            # Compute the center of the contour (centroid)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)

                # Find the farthest point from the center (likely the fingertip)
                max_dist = 0
                fingertip = None
                for point in cnt:
                    px, py = point[0]
                    dist = np.linalg.norm([px - cx, py - cy])
                    if dist > max_dist:
                        max_dist = dist
                        fingertip = (px, py)

                if fingertip:
                    cv2.circle(frame, fingertip, 8, (0, 0, 255), -1)
                    dx = fingertip[0] - cx
                    dy = fingertip[1] - cy

                    threshold = 40  # Minimum distance to consider movement
                    if abs(dx) > abs(dy):
                        if dx > threshold:
                            direccio = "RIGHT"
                        elif dx < -threshold:
                            direccio = "LEFT"
                        else:
                            direccio = None
                    else:
                        if dy > threshold:
                            direccio = "DOWN"
                        elif dy < -threshold:
                            direccio = "UP"
                        else:
                            direccio = None

                    # Display detected direction on the frame
                    if direccio:
                        cv2.putText(frame, direccio, (10, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

    # Show the result frames
    cv2.imshow("Simple Hand Detection", frame)
    cv2.imshow("Skin Mask", mask)
    
    # Press ESC to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
