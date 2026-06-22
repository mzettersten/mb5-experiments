import cv2
from PIL import Image

video_path = "laughing_baby_no_audio_grey.mp4"
out_path = "laughing_baby_no_audio_grey_firstframe.png"

cap = cv2.VideoCapture(video_path)
ok, frame = cap.read()
cap.release()

if not ok:
    raise RuntimeError("Could not read first frame")

# OpenCV gives BGR; convert to RGB
frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

Image.fromarray(frame_rgb).save(out_path)