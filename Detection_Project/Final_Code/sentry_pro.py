import cv2
import mediapipe.python.solutions.face_detection as face_logic
import os
import time
import math

# --- CONFIGURATION ---
# Eye distance threshold in pixels. 
SNOOP_THRESHOLD_PX = 45  
COOLDOWN_SECONDS = 3        
DECOY_APP_NAME = "Notes"

# --- INITIALIZATION ---
# Using model_selection=0 for short-range detection (optimized for webcams)
detector = face_logic.FaceDetection(model_selection=0, min_detection_confidence=0.5)
video_capture = cv2.VideoCapture(0)

# --- SYSTEM STATE ---
is_panicked = False
last_snoop_timestamp = 0
last_active_work_app = "Visual Studio Code"

def get_frontmost_app():
    """Queries macOS for the name of the currently active application."""
    apple_script = "osascript -e 'tell application \"System Events\" to get name of first process whose frontmost is true'"
    try:
        app_name = os.popen(apple_script).read().strip()
        return app_name
    except Exception:
        return ""

def switch_to_app(app_name):
    """Brings a specific application to the foreground."""
    apple_script = f"osascript -e 'tell application \"{app_name}\" to activate'"
    os.system(apple_script)

print("--- Sentry Pro Active ---")
print(f"Monitoring depth and application state. Decoy set to: {DECOY_APP_NAME}")

while video_capture.isOpened():
    success, frame = video_capture.read()
    if not success:
        break

    # Get frame dimensions for pixel calculation
    height, width, _ = frame.shape
    
    # AI processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = detector.process(rgb_frame)
    
    detected_face_distances = []

    if results.detections:
        for detection in results.detections:
            # Extract eye keypoints (Index 0: Right Eye, Index 1: Left Eye)
            keypoints = detection.location_data.relative_keypoints
            right_eye = (keypoints[0].x * width, keypoints[0].y * height)
            left_eye = (keypoints[1].x * width, keypoints[1].y * height)
            
            # Calculate Euclidean distance between eyes
            eye_dist = math.sqrt((right_eye[0] - left_eye[0])**2 + (right_eye[1] - left_eye[1])**2)
            detected_face_distances.append(eye_dist)

    # --- DETECTION LOGIC ---
    # A snoop is defined as any face beyond the first one that exceeds the depth threshold
    is_snoop_present = False
    if len(detected_face_distances) > 1:
        # Check all faces except the primary user (the first face detected)
        for dist in detected_face_distances[1:]:
            if dist > SNOOP_THRESHOLD_PX:
                is_snoop_present = True
                break

    if is_snoop_present:
        last_snoop_timestamp = time.time()
        if not is_panicked:
            print(f"Intrusion detected. Archiving: {last_active_work_app}")
            switch_to_app(DECOY_APP_NAME)
            is_panicked = True
    else:
        # If no snoop is present, monitor and update the current work application
        if not is_panicked:
            current_app = get_frontmost_app()
            # Only update if the current app is not the decoy or an empty string
            if current_app and current_app != DECOY_APP_NAME:
                last_active_work_app = current_app
        
        # Restoration logic after the cooldown period
        elif time.time() - last_snoop_timestamp > COOLDOWN_SECONDS:
            print(f"Environment secure. Restoring: {last_active_work_app}")
            switch_to_app(last_active_work_app)
            is_panicked = False

    # --- VISUAL FEEDBACK ---
    for i, dist in enumerate(detected_face_distances):
        label_color = (0, 0, 255) if (i > 0 and dist > SNOOP_THRESHOLD_PX) else (0, 255, 0)
        cv2.putText(frame, f"Face {i} Depth: {int(dist)}px", (20, 50 + (i * 30)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, label_color, 2)

    cv2.imshow('Sentry Pro - Security Feed', frame)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()