import cv2
import mediapipe.python.solutions.face_detection as face_logic
import os
import time

# --- SETTINGS ---
SNOOP_LIMIT = 1        # More than 1 face = Change screen
COOLDOWN_TIME = 3      # Wait 3 seconds of "silence" before restoring
DECOY_APP = "Notes"    # Spreadsheet/decoy app
WORK_APP = "Visual Studio Code" 

# --- BRAIN ---
detector = face_logic.FaceDetection(model_selection=0, min_detection_confidence=0.5)
cap = cv2.VideoCapture(0)

# --- STATE TRACKING ---
is_panicked = False
last_snoop_time = 0

print(f"Sentry ACTIVE. Protecting {WORK_APP}...")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 1. Look for faces
    results = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    current_face_count = 0
    if results.detections:
        current_face_count = len(results.detections)

    # 2. THE DECISION ENGINE
    if current_face_count > SNOOP_LIMIT:
        # --- SNOOP DETECTED ---
        last_snoop_time = time.time() # Update 'last seen' timer
        
        if not is_panicked:
            print(" SNOOP DETECTED! Hiding work...")
            # Bring Decoy to the front
            os.system(f"osascript -e 'tell application \"{DECOY_APP}\" to activate'")
            is_panicked = True

    else:
        # --- COAST IS POTENTIALLY CLEAR ---
        if is_panicked:
            # Check if it has been safe for the full Cooldown Period
            time_since_snoop = time.time() - last_snoop_time
            
            if time_since_snoop > COOLDOWN_TIME:
                print(" Coast is clear. Restoring your work...")
                # Bring Work back to the front
                os.system(f"osascript -e 'tell application \"{WORK_APP}\" to activate'")
                is_panicked = False

    # 3. Visual Feedback (Optional - you can hide this window later)
    cv2.putText(frame, f"Faces: {current_face_count}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Sentry Feed', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()