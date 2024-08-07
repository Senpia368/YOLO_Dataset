from ultralytics import YOLO

model = YOLO("models/yolov10x.pt")

results = model(source='merged_output_video.mp4', show=True, device = 'cuda:0')