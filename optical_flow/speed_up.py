import cv2 as cv
import os

# We will speed up the video so that it takes less time
video_normal = "picarx_recording.avi"
video_spedup = "picarx_recording_fast.avi"

# For that we remove every even frame
def remove_even_frames(video_normal, video_spedup):
    # Check if the input file exists
    if not os.path.exists(video_normal):
        print(f"Error: The file {video_normal} does not exist.")
        return
    
    # Open the input video
    cappie = cv.VideoCapture(video_normal)
    if not cappie.isOpened():
        print("Error: Could not open the input video.")
        return

    # Get the properties of the video
    frame_width = int(cappie.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cappie.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cappie.get(cv.CAP_PROP_FPS)
    codec = cv.VideoWriter_fourcc(*'XVID')  # You can change this to other codecs

    # Open the output video writer
    out = cv.VideoWriter(video_spedup, codec, fps, (frame_width, frame_height))

    frame_count = 0

    while cappie.isOpened():
        ret, frame = cappie.read()
        if not ret:
            break
        
        # Write every odd frame (0-based index, so 0 is first frame, 1 is second frame, etc.)
        if frame_count % 2 == 0:
            out.write(frame)

        frame_count += 1

    # Release everything when the job is finished
    cappie.release()
    out.release()
    print(f"Finished processing. Output saved to {video_spedup}")

remove_even_frames(video_normal, video_spedup)