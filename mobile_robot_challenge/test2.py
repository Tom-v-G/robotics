import cv2
import numpy as np

from scipy.stats import mode
from argparse import ArgumentParser

# Open the video file
cap = cv2.VideoCapture('Arrow Moving Right to Left Green Screen -Copyright Free.mp4')

# Get the first frame
ret, frame1 = cap.read()

# Convert the frame to grayscale
prvs = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# Create a mask for the optical flow
mask = np.zeros_like(frame1)

# Define the parameters for the optical flow algorithm
lk_params = dict(winSize=(15, 15),
                 maxLevel=4,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


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

param = {
    'pyr_scale': args['pyr_scale'],
    'levels': args['levels'],
    'winsize': args['winsize'],
    'iterations': args['iterations'],
    'poly_n': args['poly_n'],
    'poly_sigma': args['poly_sigma'],
    'flags': cv2.OPTFLOW_LK_GET_MIN_EIGENVALS
}


# Wait for a key press

while True:
    input()
    # Read the next frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculate the optical flow
    # flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, **param)

    # Convert the optical flow to polar coordinates
    # mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    mag, ang = cv2.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)

    # Scale the magnitude of the optical flow between 0 and 255
    mag_scaled = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)

    # Convert the angle to hue
    ang_degrees = ang * 180 / np.pi / 2
    print(ang_degrees)
    ang_scaled = cv2.normalize(ang_degrees, None, 0, 255, cv2.NORM_MINMAX)


    #  https://medium.com/@ggaighernt/optical-flow-and-motion-detection-5154c6ba4419
    move_sense = ang[mag > args['threshold']]
    move_mode = mode(move_sense)[0]

    print("move mode:")
    print(mag)
    print(args['threshold'])
    # print(ang)
    print(move_sense)
    print(move_mode)
    #########

    # Convert the hue and magnitude to an RGB image
    hsv = np.zeros_like(frame1)
    hsv[..., 0] = ang_scaled
    hsv[..., 1] = 255
    hsv[..., 2] = cv2.convertScaleAbs(mag_scaled)

    # Convert the HSV image to BGR
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Display the optical flow
    cv2.imshow('Optical Flow', bgr)

    # Wait for a key press
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    # Set the current frame as the previous frame for the next iteration
    prvs = next.copy()

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()