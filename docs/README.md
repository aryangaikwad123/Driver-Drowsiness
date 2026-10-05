# Drowsiness and Yawn Detection - Stage 1

This is Stage 1 of the final year Computer Engineering project: Real-time Drowsiness and Yawn Detection using Python.

## Project Overview
- Detects drowsiness by monitoring eye closure (Eye Aspect Ratio - EAR).
- Detects yawns by monitoring mouth opening (Mouth Aspect Ratio - MAR).
- Uses OpenCV, DLIB, and NumPy for computer vision.
- Runs on a PC with webcam; can be adapted for Raspberry Pi.

## Setup Instructions
1. **Prerequisites**:
   - Python 3.7+ installed.
   - Webcam available.

2. **Install Dependencies**:
   - Run: `pip install -r requirements.txt`

3. **Download Model**:
   - Download `shape_predictor_68_face_landmarks.dat` from [dlib.net](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2).
   - Place it in the `models/` folder.

4. **Run the Script**:
   - Navigate to `src/` folder.
   - Run: `python drowsiness_yawn_stage1.py`
   - Press 'q' to quit.

## Testing
- Simulate drowsiness: Close eyes partially.
- Simulate yawn: Open mouth wide.
- Record a demo video and place in `demo/`.

## Submission
- Include this folder, report (see Stage1_Report_Outline.md), and demo.
- Cite: Original video - https://youtu.be/RDuLqCT5RxY

## Next Stages
- Stage 2: Add voice alerts and Raspberry Pi integration.