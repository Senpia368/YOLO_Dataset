import os
import subprocess

# Path to the folder containing video files
video_folder_path = '20240709_Videos'
output_video_path = 'merged_output_video.mp4'

# Get a list of all video files in the folder
video_files = [f for f in os.listdir(video_folder_path) if f.endswith('.avi') or f.endswith('.mp4')]

# Ensure there are video files to process
if not video_files:
    print('No video files found in the specified folder.')
    exit()

# Create a temporary file to list all videos
with open("video_list.txt", "w") as file:
    for video_file in sorted(video_files):
        file.write(f"file '{os.path.join(video_folder_path, video_file)}'\n")

# Run ffmpeg command to concatenate videos
command = [
    'ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video_list.txt',
    '-c', 'copy', output_video_path
]

subprocess.run(command, check=True)

# Clean up
os.remove("video_list.txt")

print(f'All videos have been merged and saved to {output_video_path}')
