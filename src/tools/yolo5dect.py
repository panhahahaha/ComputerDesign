import cv2
import torch
import random
import src.tools.convert_coor as convert


class YOLODepthDetector:
    def __init__(self, model_path='yolov5s.pt', realsense=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load(r'C:\Users\huawei\ComputerDesign\yolov5-master', 'custom', path=model_path, source='local')
        self.model.to(self.device).eval()
        self.D = realsense  # RealSense 设备对象
        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(self.model.names))]

    def process_frame(self, color_frame,):
        results = self.model(color_frame)

        for *xyxy, conf, cls in results.xyxy[0]:
            if int(cls) not in [40, 39, 41]:
                continue

            label = f"{self.model.names[int(cls)]} {conf:.2f}"
            color = self.colors[int(cls)]
            cv2.rectangle(color_frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), color, 2)
            cv2.putText(color_frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            center_x = int((xyxy[0] + xyxy[2]) / 2)
            center_y = int((xyxy[1] + xyxy[3]) / 2)
            # depth = depth_frame[center_y, center_x]
            # get_real_coor = convert.pixel_to_world(center_x, center_y, 0, )

            # coor_text = f"{get_real_coor[0]:.2f} {get_real_coor[1]:.2f} {get_real_coor[2]:.2f}"
            coor_text = f"{center_x:.2f} {center_y:.2f} {30:.2f}"
            cv2.putText(color_frame, coor_text, (int(xyxy[0]), int(xyxy[1]) - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                        2)

        return color_frame

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Video Stream not open")
            return

        while True:
            ret,color_frame = cap.read()
            processed_frame = self.process_frame(color_frame)
            cv2.imshow('YOLOv5 Detection', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Example usage:
    detector = YOLODepthDetector()
    detector.run()
