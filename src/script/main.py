import Demo.src.VideoStream.D435i as D435i
import Demo.src.tools.yolo5dect as Yolo5DCT
import Demo.src.tools.FingerIdentify as FingerId
import cv2


def main():
    d435i = D435i.RealSenseD435i()
    yolo = Yolo5DCT.YOLODepthDetector()
    fingerid = FingerId.RockPaperScissors()
    while True:
        color_frame,depth_frame = d435i.get_frames()
        yolo.process_frame(color_frame,depth_frame,d435i.K)
        fingerid.detect(color_frame)
        cv2.imshow("RealSenseD435i", color_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
