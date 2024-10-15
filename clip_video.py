import cv2

def clip_video(input_file, output_file, start_time, end_time):
    # Open the video file
    cap = cv2.VideoCapture(input_file)
    
    # Get the original frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Get the width and height of the video frames
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Calculate the start and end frames based on the time (in seconds)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    
    # Define codec and create VideoWriter object to save the clipped output
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    # Set the starting frame in the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    frame_count = 0
    
    frame_number = start_frame
    while cap.isOpened():
        ret, frame = cap.read()
        
        if not ret or frame_number > end_frame:
            break
        frame_count += 1
        print(frame_count)

        # Write each frame from start_time to end_time
        out.write(frame)
        
        frame_number += 1

    # Release everything when done
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Parameters
# input_video = '/mnt/c/Users/hussa/Downloads/merged_output_video.mp4' # Path to the input video
# output_video = '/mnt/c/Users/hussa/Downloads/output_clipped_video3.mp4'  # Path to save the output video
input_video = '/mnt/c/Users/hussa/Downloads/Fusion_Yolo_Clip3.avi'
output_video = '/mnt/c/Users/hussa/Downloads/Fusion_Yolo_Clip4.mp4'

start_time = 0  # Start time in seconds
end_time = start_time+40    # End time in seconds

# Run the function
clip_video(input_video, output_video, start_time, end_time)