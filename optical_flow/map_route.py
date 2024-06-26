import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.stats import mode
from argparse import ArgumentParser

if __name__ == '__main__':
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
    ap.add_argument('-th', '--threshold', default=10.0, type=float, help='Threshold value for magnitude')
    ap.add_argument('-p', '--plot', default=False, action='store_true', help='Plot accumulators?')
    ap.add_argument('-rgb', '--rgb', default=False, action='store_true', help='Show RGB mask?')
    ap.add_argument('-s', '--size', default=10, type=int, help='Size of accumulator for directions map')

    args = vars(ap.parse_args())

    directions_map = np.zeros([args['size'], 5])
    angles_list = []
    map_list = []

    # cap = cv.VideoCapture('moving_camera_1.mp4')
    # cap = cv.VideoCapture('moving_camera_2.mp4')
    # cap = cv.VideoCapture('moving_camera_2_speed_4x.mp4')
    cap = cv.VideoCapture('moving_camera_3.mp4')
    # cap = cv.VideoCapture('car_dashcam.mp4')
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

        
        
        move_sense = ang[mag > args['threshold']]
        move_mode = mode(move_sense)[0]

        print("move_sense:", mode(move_sense))

        print("move_mode: ", move_mode)
        # angles_list.append({"angle": move_mode, "time_difference": time_difference})
        angles_list.append(move_mode)

        #map_list.append()

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
        
        text = str(move_mode)
        
        if loc in [0, 1, 2, 3]:
            locArray.append(loc)

        hsv[:, :, 0] = ang_180
        hsv[:, :, 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
        rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

        frame = cv.flip(frame, 1)
        cv.putText(frame, text, (30, 90), cv.FONT_HERSHEY_COMPLEX, frame.shape[1] / 500, (0, 0, 255), 2)

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

        #move_sense = ang[mag > args['threshold']]
        #move_mode = mode(move_sense)[0]
        # angles_list.append({"angle": move_mode, "time_difference": time_difference})
        #angles_list.append(move_mode)

        #map_list.append()

    cap.release()
    if args['record']:
        out.release()
    if args['plot']:
        plt.ioff()
    cv.destroyAllWindows()
    print(angles_list)

    print(locArray)

   



