import cv2
import mediapipe as mp
import numpy as np

class RockPaperScissors:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                                         min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def get_finger_status(self, hand_landmarks):
        fingers = []
        landmarks = hand_landmarks.landmark

        # 拇指（根据 x 坐标判断）
        fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)

        # 其他四根手指（根据 y 坐标判断）
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            fingers.append(1 if landmarks[tip].y < landmarks[pip].y else 0)

        return fingers

    def recognize_gesture(self, fingers):
        if fingers == [0, 0, 0, 0, 0]:
            return "Rock"
        elif fingers == [0, 1, 1, 0, 0]:
            return "Scissors"
        elif fingers == [1, 1, 1, 1, 1]:
            return "Paper"
        else:
            return "Unknown"

    def detect(self, frame):
        if frame is None or frame.size == 0:
            raise ValueError("Invalid input: Frame is empty or None.")

        # 确保 frame 为 numpy 数组
        if not isinstance(frame, np.ndarray):
            raise ValueError("Invalid input: Frame must be a numpy array.")
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)
        print(result)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                fingers = self.get_finger_status(hand_landmarks)
                gesture = self.recognize_gesture(fingers)
                cv2.putText(frame, gesture, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


# 运行游戏
if __name__ == "__main__":
    cap =cv2.VideoCapture(0)
    rock = RockPaperScissors()
    while True:
        ret, frame = cap.read()
        rock.detect(frame)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break