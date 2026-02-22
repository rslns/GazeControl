import cv2
import mediapipe as mp
import time
import pyautogui

pyautogui.FAILSAFE = False

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


RIGHT_IRIS = [474, 475, 476, 477]

# Eye blink landmarks
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374

# Timing
LOOK_HOLD = 1.5
ACTION_COOLDOWN = 2.5
BLINK_HOLD = 0.25

down_start = None
up_start = None
blink_start = None
last_action = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    gaze = "CENTER"
    status = ""

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark
        now = time.time()

        # ---------- IRIS (SCROLL) ----------
        iris_y = sum(lm[i].y for i in RIGHT_IRIS) / 4
        cx = int(sum(lm[i].x for i in RIGHT_IRIS) / 4 * w)
        cy = int(iris_y * h)
        cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        # ---------- SCROLL LOGIC ----------
        if iris_y > 0.6:
            gaze = "DOWN"
            if down_start is None:
                down_start = now
            elif now - down_start >= LOOK_HOLD and now - last_action >= ACTION_COOLDOWN:
                pyautogui.press("down")
                status = "NEXT VIDEO"
                last_action = now
                down_start = None

        elif iris_y < 0.45:
            gaze = "UP"
            if up_start is None:
                up_start = now
            elif now - up_start >= LOOK_HOLD and now - last_action >= ACTION_COOLDOWN:
                pyautogui.press("up")
                status = "PREVIOUS VIDEO"
                last_action = now
                up_start = None

        else:
            down_start = None
            up_start = None

        # ---------- BLINK DETECTION ----------
        left_eye_dist = abs(lm[LEFT_EYE_TOP].y - lm[LEFT_EYE_BOTTOM].y)
        right_eye_dist = abs(lm[RIGHT_EYE_TOP].y - lm[RIGHT_EYE_BOTTOM].y)
        eye_closed = left_eye_dist < 0.02 and right_eye_dist < 0.02

        if eye_closed:
            if blink_start is None:
                blink_start = now
            elif now - blink_start >= BLINK_HOLD and now - last_action >= ACTION_COOLDOWN:
                pyautogui.press("space")
                status = "PAUSE / PLAY"
                last_action = now
                blink_start = None
        else:
            blink_start = None

        # ---------- UI ----------
        cv2.putText(frame, f"Gaze: {gaze}", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, f"iris_y: {iris_y:.3f}", (30, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

        if status:
            cv2.putText(frame, status, (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 3)

    cv2.imshow("Eye + Blink Controlled Shorts", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
