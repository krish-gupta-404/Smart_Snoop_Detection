import sys
import os

print("--- M4 DEEP SCAN START ---")

try:
    import mediapipe as mp
    print(f"✅ Step 1: MediaPipe library found at: {os.path.dirname(mp.__file__)}")
    
    # We try to 'force' the solutions to load
    import mediapipe.python.solutions.face_detection as face_logic
    print("✅ Step 2: Face Detection Brain FOUND!")
    
    # Test if we can actually use it
    test_brain = face_logic.FaceDetection()
    print("✅ Step 3: Brain is ACTIVE and thinking!")

except ModuleNotFoundError:
    print("❌ Error: MediaPipe is not installed for Python 3.12.")
except AttributeError as e:
    print(f"❌ Error: Found MediaPipe, but it's empty! ({e})")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")

print("--- SCAN END ---")