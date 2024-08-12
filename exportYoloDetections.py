'''
This program saves the annotations from the yolo model in a .txt file for a set range of images in specified folder
'''
from ultralytics import YOLO
import os

# source folder
image_folder_path = 'Images'

model = model = YOLO("models/yolov10x.pt")

# index range of images
start_frame = 0
end_frame = 567

for img in os.listdir(image_folder_path)[start_frame:end_frame+1]:
    image_path = os.path.join(image_folder_path, img)
    
    # run model and save results
    results = model(source=image_path, classes=[i for i in range(8)], device = 'cuda:0', save_txt=True)
    

