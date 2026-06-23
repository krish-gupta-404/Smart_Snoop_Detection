import cv2

# This opens your built-in camera
cap = cv2.VideoCapture(0)

print("Opening camera... Press 'q' on your keyboard to close the window.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not grab a frame.")
        break

    # Show the video in a window
    cv2.imshow('Camera Test', frame)

    # If you press 'q', the loop stops
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()