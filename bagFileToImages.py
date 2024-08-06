import rosbag
import cv2
import os
from cv_bridge import CvBridge
import numpy as np
from stopwatch import Stopwatch

# Path to the bag file and output directory
bag_file_path = "/external_drive/MLK@Georgia/2024-07-09-15-23-03_0.bag"
output_video_path = 'output_video.avi'

# Initialize CvBridge
bridge = CvBridge()

# Create stopwatch to measure running time
stopwatch = Stopwatch()

# Set frame rate and resolution
fps = 60  # Frame rate of the video (assumed to be 60 FPS)
frame_size = (1920, 1080)  # Resolution of the video (width, height) - adjust as needed

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for video encoding
video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, frame_size)

stopwatch.start()
# Open the bag file
with rosbag.Bag(bag_file_path, 'r') as bag:
    # Iterate over messages
    for topic, msg, t in bag.read_messages(topics=['/axis/image_raw/compressed']):

        # Check the type of the message
        if msg._type == 'sensor_msgs/CompressedImage':
            try:
                # Decode the compressed image data
                np_arr = np.frombuffer(msg.data, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                print(img.shape)

                # Resize image if needed
                # img_resized = cv2.resize(img, frame_size)

                # Write frame to video
                video_writer.write(img)
            except Exception as e:
                print(f'Error processing message: {e}')
        else:
            print(f'Unexpected message type: {msg._type}')

# Release the VideoWriter object
video_writer.release()
stopwatch.stop()

print(f'Run time: {stopwatch.duration}')

print(f'Video saved to {output_video_path}')
