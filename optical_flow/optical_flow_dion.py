import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time
import math


from scipy.stats import mode
from argparse import ArgumentParser
import os

# docent rijdt auto gekke bochten en camera neemt op
# docent drukt op Q, en dan:
# * stopt de recording
# * wordt de video opgeslagen en ingeladen
# * de video wordt ingekort zodat hij 4 keer zo snel (en zo kort) is
# * de frames worden geanalyseerd en er wordt een mapje gemaakt
# * de angle wordt bepaald
# * de auto draait in die angle
# * de auto rijdt naar de home position


rec_flag = 'stop' # start,pause,stop
vname = None
username = os.getlogin()

                    
# make a function that takes the final x and y coordinates and returns the angle is has to make to and how far it is from the home position using pythagoras
def calc_way_back(x_coord, y_coord,gamma):
    length_back = np.sqrt((x_coord**2) + (y_coord**2))
    beta = math.atan(x_coord/y_coord)
    if gamma > beta:
        alpha = np.pi - gamma + beta # tegen klok in
    elif gamma < beta:
        alpha = - (np.pi + gamma - beta) # met de klok mee
    else: 
        alpha = np.pi
    return alpha, length_back


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

if __name__ == '__main__':
    plt.ion()
    plt.figure()
    plt.xlim(-20,20)
    plt.ylim(-20,30)

    ap = ArgumentParser()
    ap.add_argument('-rec', '--record', default=False, action='store_true', help='Record?')
    ap.add_argument('-pscale', '--pyr_scale', default=0.5, type=float,
                    help='Image scale (<1) to build pyramids for each image')
    ap.add_argument('-l', '--levels', default=3, type=int, help='Number of pyramid layers')
    ap.add_argument('-w', '--winsize', default=15, type=int, help='Averaging window size')
    ap.add_argument('-i', '--iterations', default=3, type=int,
                    help='Number of iterations the algorithm does at each pyramid level')
    ap.add_argument('-pn', '--poly_n', default=5, type=int,
                    help='Size of the pixel neighborhood used to find polynomial expansion in each pixel')
    ap.add_argument('-psigma', '--poly_sigma', default=1.1, type=float,
                    help='Standard deviation of the Gaussian that is used to smooth derivatives used as a basis for the polynomial expansion')
    ap.add_argument('-th', '--threshold', default=1., type=float, help='Threshold value for magnitude')
    ap.add_argument('-p', '--plot', default=False, action='store_true', help='Plot accumulators?')
    ap.add_argument('-rgb', '--rgb', default=False, action='store_true', help='Show RGB mask?')
    ap.add_argument('-s', '--size', default=10, type=int, help='Size of accumulator for directions map')

    args = vars(ap.parse_args())

    directions_map = np.zeros([args['size'], 5])
    angles_list = []

    # cap = cv.VideoCapture('moving_camera_1.mp4')
    # cap = cv.VideoCapture('moving_camera_2.mp4')
    # cap = cv.VideoCapture('moving_camera_2_speed_4x.mp4')
    # cap = cv.VideoCapture('moving_camera_3.mp4')
    # cap = cv.VideoCapture('car_dashcam.mp4')
    # cap = cv.VideoCapture('../../Videos/2024-05-06-12.32.33.avi')

    # cap moet het filmpje bevatten dat met "keyboard_control_record_video" is gemaakt
    cap = cv.VideoCapture(f"/home/{username}/Videos/picarx_recording_fast.avi")

    if args['record']:
        h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        codec = cv.VideoWriter_fourcc(*'MPEG')
        out = cv.VideoWriter('out.avi', codec, 10.0, (w, h))

    if args['plot']:
        plt.ion()

    frame_previous = cap.read()[1]
    gray_previous = cv.cvtColor(frame_previous, cv.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame_previous)
    hsv[:, :, 1] = 255
    param = {
        'pyr_scale': args['pyr_scale'],
        'levels': args['levels'],
        'winsize': args['winsize'],
        'iterations': args['iterations'],
        'poly_n': args['poly_n'],
        'poly_sigma': args['poly_sigma'],
        'flags': cv.OPTFLOW_LK_GET_MIN_EIGENVALS
    }

    locArray = []

    previous_timestamp = time.time();
    current_timestamp = 0

    total_displacement_x = 0
    total_displacement_y = 0
    angle = 0

    all_x_flow = []

    while True:
        grabbed, frame = cap.read()
        if not grabbed:
            break

        current_timestamp = time.time();
        time_difference = current_timestamp - previous_timestamp

        print("time difference:", time_difference)

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(gray_previous, gray, None, **param)
        mag, ang = cv.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)
        ang_180 = ang/2
        gray_previous = gray

        x_flow, y_flow = np.median(flow[:, :, 0]), np.median(flow[:, :, 1])
        all_x_flow.append(x_flow)
        print(x_flow)
        print(x_flow>.02)
        # x_flow = x_flow[x_flow > .02]
        # y_flow = y_flow[y_flow > .02]

        dt = 1
        velocity_y = np.cumsum(y_flow * dt)
        displacement_y = np.cumsum(velocity_y * dt)

        # Translate movement x field to rotation angle
        angle = angle + x_flow/(-711.6/1.57) # radians (gamma)

        x_coord = displacement_y * np.cos(angle) * np.sin(angle)
        y_coord = displacement_y * np.cos(angle)**2

        total_displacement_x += x_coord
        total_displacement_y += y_coord

        plt.scatter(total_displacement_x,total_displacement_y)

        move_sense = ang[mag > args['threshold']]
        move_mode = mode(move_sense)[0]

        print("move_sense:", mode(move_sense))
        # print(ang,mag)
        print(args['threshold'])


        print("move_mode: ", move_mode)
        # angles_list.append({"angle": move_mode, "time_difference": time_difference})
        angles_list.append(move_mode)






        if 10 < move_mode <= 100:
            directions_map[-1, 0] = 1
            directions_map[-1, 1:] = 0
            directions_map = np.roll(directions_map, -1, axis=0)
        elif 100 < move_mode <= 190:
            directions_map[-1, 1] = 1
            directions_map[-1, :1] = 0
            directions_map[-1, 2:] = 0
            directions_map = np.roll(directions_map, -1, axis=0)
        elif 190 < move_mode <= 280:
            directions_map[-1, 2] = 1
            directions_map[-1, :2] = 0
            directions_map[-1, 3:] = 0
            directions_map = np.roll(directions_map, -1, axis=0)
        elif 280 < move_mode or move_mode < 10:
            directions_map[-1, 3] = 1
            directions_map[-1, :3] = 0
            directions_map[-1, 4:] = 0
            directions_map = np.roll(directions_map, -1, axis=0)
        else:
            directions_map[-1, -1] = 1
            directions_map[-1, :-1] = 0
            directions_map = np.roll(directions_map, 1, axis=0)

        if args['plot']:
            plt.clf()
            plt.plot(directions_map[:, 0], label='Forward')
            plt.plot(directions_map[:, 1], label='Left')
            plt.plot(directions_map[:, 2], label='Backward')
            plt.plot(directions_map[:, 3], label='Right')
            plt.plot(directions_map[:, 4], label='Waiting')
            plt.legend(loc=2)
            plt.pause(1e-5)
            plt.show()

        loc = directions_map.mean(axis=0).argmax()
        if loc == 0:
            text = 'Moving forward'
        elif loc == 1:
            text = 'Moving to the left'
        elif loc == 2:
            text = 'Moving backward'
        elif loc == 3:
            text = 'Moving to the right'
        else:
            text = 'WAITING'

        text = str(displacement_y) + ', ' + str(angle)

        if loc in [0, 1, 2, 3]:
            locArray.append(loc)

        hsv[:, :, 0] = ang_180
        hsv[:, :, 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

        frame = cv.flip(frame, 1)
        cv.putText(frame, text,(30, 90), cv.FONT_HERSHEY_COMPLEX, frame.shape[1] / 500, (0, 0, 255), 2)

        k = cv.waitKey(1) & 0xff
        if k == ord('q'):
            break
        if args['record']:
            out.write(frame)
        if args['rgb']:
            cv.imshow('Mask', rgb)
        cv.imshow('Frame', frame)
        k = cv.waitKey(1) & 0xff
        if k == ord('q'):
            break

        previous_timestamp = current_timestamp

    cap.release()
    if args['record']:
        out.release()
    if args['plot']:
        plt.ioff()
    cv.destroyAllWindows()
    print(angles_list)

plt.show()

print("total_displacement_x: ", total_displacement_x)
print("total_displacement_y: ", total_displacement_y)
# print('x_flow:', all_x_flow)
all_x_flow_array = np.array(all_x_flow)
print(np.sum(all_x_flow_array[all_x_flow_array < -1]))
angle_final, length_back = calc_way_back(total_displacement_x, total_displacement_y, angle)
print('returning angle:', angle_final,'length_back:', length_back)
