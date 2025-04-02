import torch
import numpy as np
import cv2
import random
import pyrealsense2 as rs
from Demo.src.tools.convert_coor import pixel_to_world


def main():
    D = RealSenseD435i()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.hub.load('/home/p/yolov5', 'custom', path='../tools/yolov5s.pt', source='local')
    model.to(device).eval()
    cap = cv2.VideoCapture(0)
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(model.names))]
    if not cap.isOpened():
        print("Video Stream not open")
        return
    while True:
        color_frame, depth_frame = D.get_frames()
        # print(color_frame)
        # Identify
        results = model(color_frame)
        D.draw_axis(color_frame)
        for *xyxy, conf, cls in results.xyxy[0]:
            if int(cls) not in [40, 39, 41]:
                continue
            label = f"{model.names[int(cls)]} {conf:.2f}"
            color = colors[int(cls)]
            cv2.rectangle(color_frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
            cv2.putText(color_frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            center_x = int((xyxy[0] + xyxy[2]) / 2)
            center_y = int((xyxy[1] + xyxy[3]) / 2)
            # print(depth_frame.shape)
            depth = depth_frame[center_y, center_x]
            # print(depth)
            # print("depth.shape:", depth.shape)
            get_real_coor = pixel_to_world(center_x, center_y, depth, D.K)
            # print(label, get_real_coor)
            coor_text = f"{get_real_coor[0]:.2f} {get_real_coor[1]:.2f} {get_real_coor[2]:.2f}"
            cv2.putText(color_frame, coor_text, (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        color, 2)
        cv2.imshow('YOLOv5 Detection', color_frame)
        # cv2.imwrite("output/demo0.jpg", color_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


class RealSenseD435i:
    def __init__(self):
        print("Starting D435i... ~~~~")
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # 启用 RGB 和 深度流
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgba8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        try:
            # 启动相机
            self.pipeline.start(self.config)

            # 获取相机内参
            profile = self.pipeline.get_active_profile()
            depth_stream = profile.get_stream(rs.stream.depth)
            intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()

            # 相机内参矩阵 K
            self.K = np.array([
                [intrinsics.fx, 0, intrinsics.ppx],
                [0, intrinsics.fy, intrinsics.ppy],
                [0, 0, 1]
            ])
            print("starting successed!")
            print("RealSense D435i 内参矩阵 K:")
            print(self.K)
        except:
            print("Starting failed!")
            return

    def stop(self):
        """ 停止相机流 """
        self.pipeline.stop()
        print("相机已停止")

    def get_frames(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        color_image = np.asanyarray(color_frame.get_data())
        depth_frame = np.asanyarray(depth_frame.get_data())
        return color_image, depth_frame
        # 创建相机对象并获取 K

    def draw_axis(self, frame):
        x = int(self.K[0, 2])
        y = int(self.K[1, 2])
        color = (0, 255, 0)
        cv2.line(frame, (0, y), (640, y), (0, 255, 0), 2, )  # 画水平线（y固定）
        cv2.line(frame, (x, 0), (x, 480), (0, 255, 0), 2, )  # 画垂直线（x固定）


main()
