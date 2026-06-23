# SMART SNOOP DETECTION
A real-time macOS privacy utility that uses MediaPipe computer vision to track face count and proximity. When a second person leans into view, the script automatically hides your active window behind a decoy app, restoring your workspace only when the coast is clear.

---

## TECHNICAL ARCHITECTURE

### 1. Machine Flow
The script functions as a state machine, tracking safety states and caching your active workspace.

* **Normal State:** Logs your active application once per second while you work alone.
* **Panic State:** Freezes window logging and forces the decoy application to the front.

### 2. Proximity Filtering
To filter out background movement, the system applies the Euclidean distance formula to MediaPipe facial landmark vectors:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$

The script measures the pixel distance between eyes ($d$). Background movement yields a low value, while a snoop leaning over your shoulder triggers the threshold.

---

## REQUIREMENTS AND PERMISSIONS

* **OS:** macOS 12.0 (Monterey) or higher
* **Processor:** Apple Silicon (M1, M2, M3, M4)
* **Hardware:** FaceTime HD camera or USB webcam


> **Note:** Your terminal or IDE requires **Camera** access to process video and **Accessibility** permissions to allow AppleScript window control.

---

## HOW TO START?

###  - Installation
git clone [https://github.com/yourusername/snoop-sentry.git](https://github.com/yourusername/snoop-sentry.git)

cd snoop-sentry

python3.12 -m pip install opencv-python mediapipe==0.10.13 --break-system-packages

### - Configuration 
SNOOP_THRESHOLD_PX = 45   (Pixel distance between eyes. Increase to reduce sensitivity.)

COOLDOWN_SECONDS = 3     (Wait duration before restoring your original workspace.)

DECOY_APP_NAME = "Notes"    (The target application used to mask your screen.)

---

## USAGE
1) Open your designated decoy application (e.g., Notes) and leave it running in the background.
2) Navigate to your project folder and launch the script:
   {python3.12 sentry_pro.py}
3) Click back into your active workspace (e.g., VS Code, Safari).
4) To Exit: Press q while focused on the video window, or press Ctrl + C in your terminal window.
