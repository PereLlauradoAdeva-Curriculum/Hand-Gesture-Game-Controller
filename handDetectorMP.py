import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw  = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7,
                                         min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)
        self.threshold = 20
        self.direccio = None

    def get_direction(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape
        small = cv2.resize(frame, (w//2, h//2), interpolation=cv2.INTER_AREA)
        small = cv2.GaussianBlur(small, (5,5), 0)
        img_rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        res = self.hands.process(img_rgb)

        self.direccio = None
        if res.multi_hand_landmarks:
            lm = res.multi_hand_landmarks[0]
            ws = lm.landmark[self.mp_hands.HandLandmark.WRIST]
            ts = lm.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            wx, wy = int(ws.x * (w//2)), int(ws.y * (h//2))
            tx, ty = int(ts.x * (w//2)), int(ts.y * (h//2))
            dx, dy = tx - wx, ty - wy

            if abs(dx) > abs(dy):
                if dx >  self.threshold: self.direccio = "RIGHT"
                elif dx < -self.threshold: self.direccio = "LEFT"
            else:
                if dy >  self.threshold: self.direccio = "DOWN"
                elif dy < -self.threshold: self.direccio = "UP"

            # Dibuixa la mà i la direcció
            self.mp_draw.draw_landmarks(frame, lm, self.mp_hands.HAND_CONNECTIONS)
            if self.direccio:
                cv2.putText(frame, self.direccio, (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        # ✅ Mostra la finestra amb la càmera
        cv2.imshow("Direcció de la mà", frame)
        cv2.waitKey(1)  # necessari per refrescar finestra

        return self.direccio

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
