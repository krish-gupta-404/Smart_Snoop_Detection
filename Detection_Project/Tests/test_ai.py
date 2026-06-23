import cv2
import mediapipe.python.solutions.face_detection as face_logic

# Initialize the M4 Brain
detector = face_logic.FaceDetection(model_selection=0, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

print("Opening AI Vision... Press 'q' to quit.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # Convert to RGB for the AI
    results = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.detections:
        # Draw green boxes around EVERY face it sees
        for detection in results.detections:
            # This is a built-in helper to draw the boxes for us
            import mediapipe.python.solutions.drawing_utils as drawing
            drawing.draw_detection(frame, detection)
            
        cv2.putText(frame, f"Faces: {len(results.detections)}", (20, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow('M4 Face Recognition Test', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()