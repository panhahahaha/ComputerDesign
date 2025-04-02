import pyrealsense2 as rs
import numpy as np
import cv2


class RealSenseD435i:
    def __init__(self):
        print("Starting D435i... ~~~~")
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        # 启用 RGB 和 深度流
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        try:
            # 启动相机
            self.profile = self.pipeline.start(self.config)

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

    def read(self):
        """
        适配cv2中的方法
        """

        return self.get_frames()

    def isOpened(self):
        return self.profile.get_device()

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
        return depth_frame, color_image
        # 创建相机对象并获取 K

    def draw_axis(self, frame):
        x = int(self.K[0, 2])
        y = int(self.K[1, 2])
        color = (0, 255, 0)
        cv2.line(frame, (0, y), (640, y), (0, 255, 0), 2, )  # 画水平线（y固定）
        cv2.line(frame, (x, 0), (x, 480), (0, 255, 0), 2, )  # 画垂直线（x固定）
