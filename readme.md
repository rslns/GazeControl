Eye & Blink Controlled Shorts Scroller
->Project Overview
This project is a Python-based computer vision application that allows users to control short-form videos (YouTube Shorts, Instagram Reels, etc.) using:
Eye gaze (look up / look down)
Blink detection (pause/play)
The system uses webcam input to detect facial landmarks and trigger keyboard events for scrolling and playback control.

->Technologies Used

-> Programming Language
Python 3.11 (Recommended)
MediaPipe is unstable on Python 3.13+

->Libraries
OpenCV
Used for:
Accessing webcam
Frame processing
Drawing UI elements
Install:
pip install opencv-python
MediaPipe
Used for:
Face mesh detection
Iris tracking
Blink detection using facial landmarks
Install:
pip install mediapipe==0.10.9
(Important: Some newer versions remove mp.solutions)
PyAutoGUI
Used for:
Simulating keyboard presses
Controlling video scroll and pause
Install:
pip install pyautogui

->Hardware Requirements
Windows PC
Webcam (internal or external)
Stable lighting
Minimum 720p camera recommended

-> System Requirements
Windows 10 / 11
Python 3.11.x
Camera access enabled:
Settings → Privacy & Security → Camera
Enable camera access for desktop apps
How It Works ?
->Gaze Detection
The system tracks iris landmark points using MediaPipe FaceMesh.
If iris Y-position > threshold → NEXT video
If iris Y-position < threshold → PREVIOUS video
Threshold values are manually tuned.

->Blink Detection
Distance between upper and lower eyelid landmarks is calculated.
If:
distance < blink_threshold
And blink duration > minimum hold time
→ Spacebar is pressed (Pause / Play)
->Action Control Logic
To prevent accidental scrolling:
Gaze must be held for 1.5 seconds
Cooldown between actions: 2.5 seconds
Blink must be intentional (0.25s hold)

python eye_scroll.py

Keep browser window active
Look up/down to navigate
Blink to pause
Press ESC to exit.
-> Limitations

Sensitive to lighting conditions
Requires face centered in frame
Hardcoded thresholds (may need tuning per user)
Works only if browser window is active
Performance depends on camera quality
-> Known Issues
Random triggering if face too close
Iris tracking unstable under low light
Different face shapes require threshold adjustment
-> Possible Improvements
Auto-calibration of neutral gaze
Smoothing filter for iris movement
GUI for threshold adjustment
Convert into background Windows application
Add left/right gaze detection
->Use Cases
Hands-free browsing
Accessibility support
Gesture-controlled interfaces
Experimental HCI (Human-Computer Interaction) project
