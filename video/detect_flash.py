import os
import cv2
import numpy as np

def detect_flash_frame(frames_dir: str) -> tuple[int, list[float]]:
    frame_files = sorted(os.listdir(frames_dir))
    brightness_values = []

    for filename in frame_files:
        path = os.path.join(frames_dir, filename)
        frame = cv2.imread(path)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        brightness_values.append(brightness)

    diffs = np.diff(brightness_values)
    flash_frame = int(np.argmax(diffs) + 1)
    return flash_frame, brightness_values
