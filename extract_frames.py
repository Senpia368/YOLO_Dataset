'''
This program takes in the start and end times as input and extracts every set number of frames within the interval
'''
import cv2
import os

def getFrameRange():
    '''
        takes starting time and ending time as input
        returns tuple with starting frame and ending frame
    '''
    start_minute = int(input('Enter starting minute: '))
    start_second = int(input('Enter starting second: '))

    end_minute = int(input('Enter ending minute: '))
    end_second = int(input('Enter ending minute: '))

    start_second += start_minute*60
    end_second += end_minute*60

    start_frame = start_second*60
    end_frame = end_second*60

    return (start_frame, end_frame)

video_path = "merged_output_video.mp4"

destination_path = 'Images'
os.makedirs(destination_path, exist_ok=True)

start_frame, end_frame = getFrameRange()

save_interval = 15

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print('Error: Could not open video.')
    exit()

cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

current_frame = start_frame
saved_frame_count = 0

while current_frame <= end_frame:
    ret, frame = cap.read()

    # break loop if there are no more frames
    if not ret:
        break

    # Save the frame at the specified interval
    if (current_frame - start_frame) % save_interval == 0:
        frame_filename = os.path.join(destination_path, f'frame_{current_frame}.jpg')
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1

    current_frame += 1

# Release the video capture object
cap.release()

print(f"Saved {saved_frame_count} frames to {destination_path}")



    
