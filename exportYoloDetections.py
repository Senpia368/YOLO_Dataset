'''
This program saves the annotations from the yolo model in a .txt file for a set range of images in specified folder
'''
from ultralytics import YOLO
import os

def cleanupFolder(folder_path, fileType):
    '''This function removes unwanted files with the specified type in the folder'''
    for i in os.listdir(folder_path):
        if i.split('.')[-1] == fileType:
            file_path = os.path.join(folder_path,i)
            os.remove(file_path)
# source folder
image_folder_path = 'task_task 1_dataset_2024_08_08_19_07_23_yolo 1.1/obj_train_data'

cleanupFolder(image_folder_path, 'txt')

model = model = YOLO("models/yolov10x.pt")

# index range of images
start_frame = 0
end_frame = 567

for img in os.listdir(image_folder_path)[start_frame:end_frame+1]:
    image_path = os.path.join(image_folder_path, img)
    
    # run model and save results
    results = model(source=image_path, classes=[i for i in range(8)], device = 'cuda:0', save_txt=True)
    

