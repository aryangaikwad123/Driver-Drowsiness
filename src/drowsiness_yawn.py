import json
import os
import time
from datetime import datetime

import cv2
import dlib
import geocoder
import numpy as np
import pygame
from imutils import face_utils


# ================= PATHS =================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
ALARM_PATH = os.path.join(BASE_DIR, "alarm.wav")
PREDICTOR_PATH = (
    "/Users/aryangaikwad/Desktop/Drowsiness Detection/models/"
    "shape_predictor_68_face_landmarks.dat"
)


# ================= SOUND =================

alarm_sound = None

try:
    pygame.mixer.init()
    if os.path.exists(ALARM_PATH):
        alarm_sound = pygame.mixer.Sound(ALARM_PATH)
    else:
        print(f"Warning: alarm sound not found at {ALARM_PATH}")
except pygame.error as error:
    print(f"Warning: pygame audio could not be initialized: {error}")


# ================= DASHBOARD FUNCTIONS =================

def send_photo(frame):
    os.makedirs(DASHBOARD_DIR, exist_ok=True)
    img_path = os.path.join(DASHBOARD_DIR, "alert.jpg")
    cv2.imwrite(img_path, frame)


def get_location():
    try:
        g = geocoder.ip("me")
        if g.ok and g.latlng:
            return g.latlng
    except Exception as error:
        print(f"Warning: could not get location: {error}")

    return None


def update_dashboard(status, location, drowsy_count, yawn_count):
    os.makedirs(DASHBOARD_DIR, exist_ok=True)

    data = {
        "status": status,
        "location": location,
        "drowsy_count": drowsy_count,
        "yawn_count": yawn_count,
        "last_alert": str(datetime.now()),
        "image": "alert.jpg",
    }

    dashboard_file = os.path.join(DASHBOARD_DIR, "data.json")

    with open(dashboard_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_map_link():
    location = get_location()

    if location:
        lat, lon = location
        return f"https://www.google.com/maps?q={lat},{lon}"

    return "Location unavailable"


# ================= DLIB =================

if not os.path.exists(PREDICTOR_PATH):
    raise FileNotFoundError(
        "Could not find dlib landmark predictor file at: "
        f"{PREDICTOR_PATH}"
    )

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

(l_start, l_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(r_start, r_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(m_start, m_end) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# ================= FUNCTIONS =================

def eye_aspect_ratio(eye):
    a = np.linalg.norm(eye[1] - eye[5])
    b = np.linalg.norm(eye[2] - eye[4])
    c = np.linalg.norm(eye[0] - eye[3])

    if c == 0:
        return 0

    return (a + b) / (2.0 * c)


def mouth_aspect_ratio(mouth):
    a = np.linalg.norm(mouth[2] - mouth[10])
    b = np.linalg.norm(mouth[4] - mouth[8])
    c = np.linalg.norm(mouth[0] - mouth[6])

    if c == 0:
        return 0

    return (a + b) / (2.0 * c)


# ================= THRESHOLDS =================

EYE_AR_THRESH = 0.25
MOUTH_AR_THRESH = 0.80
DROWSY_TIME_THRESH = 5
YAWN_TIME_THRESH = 5
ALERT_INTERVAL = 5
DASHBOARD_UPDATE_INTERVAL = 2


# ================= STATE =================

eyes_closed_start = None
mouth_open_start = None
drowsy_count = 0
yawn_count = 0
last_alert_time = 0
last_yawn_alert_time = 0
last_dashboard_update = 0
yawn_active = False


# ================= VIDEO =================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    raise SystemExit(1)

print("Starting real-time detection. Press 'q' to quit.")


# ================= MAIN LOOP =================

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    drowsy_detected = False
    yawn_detected = False
    ear = 0
    mar = 0

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        left_eye = shape[l_start:l_end]
        right_eye = shape[r_start:r_end]
        mouth = shape[m_start:m_end]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        ear = (left_ear + right_ear) / 2.0
        mar = mouth_aspect_ratio(mouth)

        cv2.drawContours(frame, [cv2.convexHull(left_eye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(right_eye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(mouth)], -1, (255, 0, 0), 1)
         # ================= DROWSINESS =================

        if ear < EYE_AR_THRESH:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()

            closed_duration = time.time() - eyes_closed_start

            if closed_duration >= DROWSY_TIME_THRESH:
                drowsy_detected = True
        else:
            eyes_closed_start = None

        # ================= YAWN =================

        if mar > MOUTH_AR_THRESH:
            if mouth_open_start is None:
                mouth_open_start = time.time()

            mouth_open_duration = time.time() - mouth_open_start

            if mouth_open_duration >= YAWN_TIME_THRESH:
                yawn_detected = True

                if not yawn_active:
                    yawn_count += 1
                    yawn_active = True
        else:
            mouth_open_start = None
            yawn_active = False

    # ================= ALERT SYSTEM =================

    if drowsy_detected:
        if (
            alarm_sound is not None
            and pygame.mixer.get_init()
            and not pygame.mixer.get_busy()
        ):
            alarm_sound.play()

        if time.time() - last_alert_time > ALERT_INTERVAL:
            drowsy_count += 1
            send_photo(frame)
            update_dashboard("Drowsy", get_map_link(), drowsy_count, yawn_count)
            last_alert_time = time.time()
    elif yawn_detected:
        if (
            alarm_sound is not None
            and pygame.mixer.get_init()
            and not pygame.mixer.get_busy()
        ):
            alarm_sound.play()

        if time.time() - last_yawn_alert_time > ALERT_INTERVAL:
            send_photo(frame)
            update_dashboard("Yawning", get_map_link(), drowsy_count, yawn_count)
            last_yawn_alert_time = time.time()
    else:
        if pygame.mixer.get_init():
            pygame.mixer.stop()

        if time.time() - last_dashboard_update > DASHBOARD_UPDATE_INTERVAL:
            update_dashboard("Normal", get_map_link(), drowsy_count, yawn_count)
            last_dashboard_update = time.time()
# ================= DISPLAY =================

    if eyes_closed_start is not None:
        closed_duration = time.time() - eyes_closed_start

        cv2.putText(
            frame,
            f"Eyes Closed: {closed_duration:.1f}s",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

    if mouth_open_start is not None:
        mouth_open_duration = time.time() - mouth_open_start

        cv2.putText(
            frame,
            f"Mouth Open: {mouth_open_duration:.1f}s",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )

    if drowsy_detected:
        cv2.putText(
            frame,
            "DROWSINESS DETECTED!",
            (10, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    if yawn_detected:
        cv2.putText(
            frame,
            "YAWN DETECTED!",
            (10, 120 if not drowsy_detected else 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )

    cv2.putText(
        frame,
        f"Drowsy Count: {drowsy_count}",
        (10, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"Yawn Count: {yawn_count}",
        (10, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"EAR: {ear:.2f}",
        (300, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        f"MAR: {mar:.2f}",
        (300, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Drowsiness Detection - Final", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Detection stopped.")
