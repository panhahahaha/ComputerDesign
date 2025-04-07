import cv2
import mediapipe as mp
import math
import src.VideoStream.D435i as D435i
import src.VideoStream.ImageStream as ImageStream
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
# Open a video stream (for example, webcam)
# cap = D435i.RealSenseD435i()
path = "/home/p/yolov5/Demo/TestImage/FallDownImage"


def empty(x):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 480)
cv2.createTrackbar("Angle", "Parameters", 0, 180, empty)


def calculate_angle(a, b, c):
    """ 计算三点形成的角度 """
    a = np.array(a)  # x, y
    b = np.array(b)
    c = np.array(c)

    # 计算向量
    ab = a - b
    bc = c - b

    # 计算角度
    angle = np.arccos(np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc)))
    return np.degrees(angle)


def main():
    img = ImageStream.ImageStream(path)
    images = img.read_image()
    for index, frame in enumerate(images):
        # 处理图像，进行骨骼识别
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            # 绘制骨架
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # 获取关键点坐标
            landmarks = results.pose_landmarks.landmark
            # 比如可以获取脚踝、膝盖、臀部、肩膀、头等关键点坐标
            ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
            knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
            hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]

            # 可以计算角度，判断是否摔倒
            angle = calculate_angle(ankle_left, knee_left, hip_left)
            real = cv2.getTrackbarPos("Angle", "Parameters")
            # 假设当膝盖角度小于30度时，可能是摔倒的姿势
            if angle < real:
                cv2.putText(frame, 'Fall detected!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                img.write_image(frame, str(index))
        if cv2.waitKey(1) & 0xFF == ord('n'):
            break
    print(images)


if __name__ == "__main__":
    main()
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#
#     # Convert frame to RGB for MediaPipe
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = pose.process(rgb_frame)
#
#     # Draw pose landmarks on the frame
#     if results.pose_landmarks:
#         mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#
#         # Extract landmarks
#         landmarks = results.pose_landmarks.landmark
#
#         # Get key points (example: shoulder, hip, knee, ankle)
#         shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
#         hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
#         knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
#         ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
#
#         # Calculate the angle between the torso (hip to shoulder) and the thigh (knee to hip)
#         angle = math.degrees(
#             math.atan2(knee.y - hip.y, knee.x - hip.x) - math.atan2(shoulder.y - hip.y, shoulder.x - hip.x)
#         )
#
#         # If the angle is too extreme, it might indicate a fall
#         if abs(angle) > 45:  # Threshold for fall detection
#             cv2.putText(frame, "Fall Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#
#     # Show the frame with detected pose
#     cv2.imshow('Pose Detection', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
