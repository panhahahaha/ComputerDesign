import cv2
import mediapipe as mp
import math

# 初始化 MediaPipe Pose
# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()
# import numpy as np

# 检测摔倒的阈值（需要根据实际情况进行调整）
ANGLE_THRESHOLD = 70  # 用于检测人体直立的角度阈值

#
# class FallDetectorQueue:
#     def __init__(self, buffersize=5, threshold=1):
#         self.__buffersize = buffersize
#         self.__threshold = threshold
#         self.y_value_history = np.zeros(buffersize, dtype=np.uint8)
#         self.index = 0
#
#     def change_buffersize(self, buffersize):
#         self.__buffersize = buffersize
#
#     def change_threshold(self, threshold):
#         self.__threshold = threshold
#
#     def add_frames(self, y_values):
#         max_previous = np.max(self.y_value_history)
#         if max_previous - y_values > self.__threshold:
#             print("可能摔倒")
#             return True
#         self.y_value_history[self.index] = y_values
#         self.index = (self.index + 1) % self.__buffersize
#
#
def empty(x):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 480)
cv2.createTrackbar("Angle", "Parameters", 0, 180, empty)
cv2.createTrackbar("body_ground_angle", "Parameters", 75, 180, empty)
cv2.createTrackbar("error_threshold", "Parameters", 0, 1, empty)
cv2.createTrackbar("velocity", "Parameters", 0, 1, empty)
# fall_detector = FallDetectorQueue()


def calculate_angle(a, b, c):
    """计算三点之间的角度"""
    print("a:", a, "b:", b, "c:", c)
    angle = math.degrees(
        math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    )
    # print("origin angle: ", angle)
    return angle


def judgment_method(landmarks):
    falled = False
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]  # 对应每个列表的索引
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y]
    nose = [landmarks[mp_pose.PoseLandmark.NOSE].x, landmarks[mp_pose.PoseLandmark.NOSE].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
    right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE].y]

    def calculate_torso_angle(left_shoulder, right_shoulder, left_hip, right_hip):
        body_ground_angle_threshold = cv2.getTrackbarPos("body_ground_angle", "Parameters")
        # print(body_ground_angle_threshold)
        # 计算肩膀中心点
        shoulder_mid = [(left_shoulder[0] + right_shoulder[0]) / 2,
                        (left_shoulder[1] + right_shoulder[1]) / 2]

        # 计算臀部中心点
        hip_mid = [(left_hip[0] + right_hip[0]) / 2,
                   (left_hip[1] + right_hip[1]) / 2]

        # 计算躯干与地面的角度
        body_ground_angle = calculate_angle(shoulder_mid, hip_mid, [hip_mid[0], hip_mid[1] + 1])
        if body_ground_angle > body_ground_angle_threshold:
            return True

    def nose_ankle_position(left_ankle, right_ankle, nose):
        mid_x = (left_ankle[0] + right_ankle[0]) / 2
        mid_y = (left_ankle[1] + right_ankle[1]) / 2
        print("mid y:", mid_y, "nose y:", nose[0])
        error_threshold = cv2.getTrackbarPos("error_threshold", "Parameters")
        if nose[1] > mid_y:
            return True

    # def velocity(left_hip, right_hip):
    #     speed = cv2.getTrackbarPos("velocity", "Parameters")
    #     mid_x = (left_hip[0] + right_hip[0]) / 2
    #     mid_y = (left_hip[1] + right_hip[1]) / 2
    #     fall_detector.change_threshold(speed)
    #
    #     return fall_detector.add_frames(mid_y)

    # falled = calculatxcfe_torso_angle(left_shoulder, right_shoulder, left_hip, right_hip)
    # falled = nose_ankle_position(left_ankle, right_ankle, nose)
    falled = velocity(left_hip, right_hip)

    return falled
    # 读取视频流


def main():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 进行姿态估计
        results = pose.process(frame)

        # 如果检测到人体关键点
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # 检测是否摔倒
            if judgment_method(results.pose_landmarks.landmark):
                cv2.putText(frame, "Fall detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # 显示结果
        cv2.imshow('Pose Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
