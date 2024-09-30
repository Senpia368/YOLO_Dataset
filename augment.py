import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
import numpy as np
import os

# Function to parse YOLO format labels
def parse_yolo_labels(label_file):
    with open(label_file, 'r') as file:
        labels = []
        for line in file.readlines():
            class_id, cx, cy, w, h = map(float, line.strip().split())
            labels.append([class_id, cx, cy, w, h])
    return labels

# Function to convert from YOLO (normalized) format to Albumentations format (Pascal VOC)
def yolo_to_voc(bboxes, image_width, image_height):
    voc_bboxes = []
    for bbox in bboxes:
        class_id, cx, cy, w, h = bbox
        # Convert to Pascal VOC format (x_min, y_min, x_max, y_max)
        x_min = (cx - w / 2) * image_width
        y_min = (cy - h / 2) * image_height
        x_max = (cx + w / 2) * image_width
        y_max = (cy + h / 2) * image_height
        voc_bboxes.append([x_min, y_min, x_max, y_max, class_id])
    return voc_bboxes

# Function to convert back from Albumentations (Pascal VOC) format to YOLO format
def voc_to_yolo(bboxes, image_width, image_height):
    yolo_bboxes = []
    for bbox in bboxes:
        x_min, y_min, x_max, y_max, class_id = bbox
        # Convert back to YOLO format (cx, cy, w, h) normalized
        cx = ((x_min + x_max) / 2) / image_width
        cy = ((y_min + y_max) / 2) / image_height
        w = (x_max - x_min) / image_width
        h = (y_max - y_min) / image_height
        yolo_bboxes.append([class_id, cx, cy, w, h])
    return yolo_bboxes

# Function to apply augmentation and save the new image and labels
def augment_image_and_labels(image_path, label_file, output_dir):
    # Load image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Parse YOLO labels
    labels = parse_yolo_labels(label_file)

    # Convert YOLO labels to VOC format for Albumentations
    bboxes = yolo_to_voc(labels, width, height)

    # Define the augmentation pipeline
    transform = A.Compose([
        A.RandomSizedBBoxSafeCrop(width=width, height=height, p=0.5),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.5),
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels']))

    # Augment the image and bounding boxes
    transformed = transform(image=image, bboxes=[bbox[:4] for bbox in bboxes], class_labels=[bbox[4] for bbox in bboxes])

    augmented_image = transformed['image']
    augmented_bboxes = transformed['bboxes']
    augmented_class_labels = transformed['class_labels']

    # Convert the augmented bounding boxes back to YOLO format
    yolo_bboxes = voc_to_yolo([list(bbox) + [label] for bbox, label in zip(augmented_bboxes, augmented_class_labels)], width, height)

    # Save the augmented image
    image_filename = os.path.basename(image_path)
    image_output_path = os.path.join(output_dir, f'augmented_{image_filename}')
    cv2.imwrite(image_output_path, augmented_image)

    # Save the updated labels in YOLO format
    label_output_path = os.path.join(output_dir, f'augmented_{os.path.basename(label_file)}')
    with open(label_output_path, 'w') as file:
        for bbox in yolo_bboxes:
            class_id, cx, cy, w, h = bbox
            file.write(f'{int(class_id)} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}\n')

    print(f'Augmented image saved to {image_output_path}')
    print(f'Augmented labels saved to {label_output_path}')


if __name__ == "__main__":
    # Example usage
    image_path = 'path/to/image.jpg'
    label_file = 'path/to/labels.txt'
    output_dir = 'path/to/output'
    augment_image_and_labels(image_path, label_file, output_dir)
