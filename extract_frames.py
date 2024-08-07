import cv2

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




    
