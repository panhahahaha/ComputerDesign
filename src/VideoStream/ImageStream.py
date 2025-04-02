import os
import cv2
from typing import List
import numpy as np


class ImageStream:
    def __init__(self, path: str):
        self.path = path  # Store the base path
        self.images: List[str] = [f for f in os.listdir(path) if
                                  f.lower().endswith(('.png', '.jpg', '.jpeg'))]  # Filter for image files
        self.index = len(self.images)
        print(f"Images found: {self.images}")

    def read_image(self) -> List[np.ndarray]:
        color_frames: List[np.ndarray] = []
        for image_name in self.images:
            image_path = os.path.join(self.path, image_name)  # Combine path and image name
            image = cv2.imread(image_path)
            if image is not None:
                color_frames.append(image)
            else:
                print(f"Failed to read image: {image_path}")
        return color_frames

    def write_image(self, image: np.ndarray, filename: str):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filename += '.jpg'  # Default to '.jpg' if no extension
        output_path = os.path.join("/home/p/yolov5/Demo/output", filename)  # Combine directory and filename
        success = cv2.imwrite(output_path, image)
        if success:
            print(f"Image saved to {output_path}")
        else:
            print(f"Failed to save image to {output_path}")

    def __next__(self):
        return cv2.imread(os.path.join(self.path, self.images[self.index]))

    def __iter__(self):
        return self
