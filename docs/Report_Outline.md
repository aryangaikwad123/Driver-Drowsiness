# Stage 1 Report: Drowsiness and Yawn Detection

## 1. Introduction
- Problem Statement: Drowsiness and yawning can indicate fatigue, especially in drivers.
- Objective: Implement basic real-time detection using Python.
- Relevance: Computer vision for safety applications.

## 2. Methodology
- Libraries: OpenCV (video processing), DLIB (facial landmarks), NumPy (calculations).
- Algorithms:
  - EAR: (Vertical eye distances) / Horizontal eye distance.
  - MAR: Vertical mouth distance / Horizontal mouth distance.
- Thresholds: EAR < 0.25 for drowsiness; MAR > 0.6 for yawn.

## 3. Implementation
- Code Structure: See `src/drowsiness_yawn_stage1.py`.
- Setup Steps: As in README.md.

## 4. Results
- Screenshots: Include images of detection overlays.
- Demo Video: Link to `demo/demo.mp4`.
- Accuracy: Tested in good lighting; thresholds adjustable.

## 5. Challenges
- DLIB installation issues; lighting sensitivity.

## 6. Conclusion and Future Work
- Achieved basic detection.
- Stage 2: Voice alerts, optimization for Raspberry Pi.

## Appendices
- Full Code: Attached.
- References: YouTube video, DLIB docs.