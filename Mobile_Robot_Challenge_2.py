'''
Automatic Control of Robot via SSH
'''

from lib.SSH import SSH
from lib.FlowAnalyzer import process_video, calc_way_back_live, polar_way_back
from time import sleep

import readchar
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TKAgg', force=True)

if __name__=='__main__':
    ssh = SSH()
    ssh.run_channel_command('cd picar-x/Project')
    ssh.run_channel_command('python3')
    ssh.run_channel_command('from Robot import Robot')
    ssh.run_channel_command('robot = Robot()')

    # Activate Manual Mode

    print('Activating Robot')
    sleep(5)
    print('Activating Camera')
    counter = 0
    drive_video_file = f'drive'
    ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')")
    sleep(1)
    
    print('''
    Press keys on keyboard to control PiCar-X!
        w: Forward
        a: Turn left
        s: Backward
        d: Turn right
        q: Go to HP
''')
    
    while True:
        key = readchar.readkey()
        key = key.lower()
        if key in('wsadq'): 
            if 'w' == key:
                ssh.run_channel_command('robot.drive_forward()')
            elif 's' == key:
                ssh.run_channel_command('robot.drive_backward()')
            elif 'a' == key:
                ssh.run_channel_command('robot.turn_left()')
            elif 'd' == key:
                ssh.run_channel_command('robot.turn_right()')
            elif 'q' == key:
                print('Exiting manual mode')
                break
            sleep(0.7)
            ssh.run_channel_command('robot.stop()')
    print('Stopping camera')
    ssh.run_channel_command('robot.stop_camera()')
    sleep(1)
    ssh.download_file(f'Videos/{drive_video_file}_{counter}.avi', f'temp/{drive_video_file}_{counter}.avi')
    sleep(1)
    R = 0
    phi = 0

    x_curr, y_curr, angle_curr, R, phi, orientation = process_video(f'{drive_video_file}_{counter}', crop=0.5)
    print(R, phi)
    x_curr_plot = (x_curr * 47) / -1.715769835273885 
    y_curr_plot = (y_curr * 137) / -2.206988055799586 
    angle_curr_plot = (angle_curr * 0.296705972839036) / 0.09911910495023506

    # length_back, target_angle, delta = calc_way_back_live(x_curr_plot, y_curr_plot, angle_curr_plot)
    target_angle, delta = polar_way_back(orientation,phi)

    counter += 1

    x_list = [0, x_curr_plot]
    y_list = [0, y_curr_plot]
    R_list = [0, R[0]]
    phi_list = [0, phi[0]]

    
    # _________________________________________

    #      Finding and touching object
    #  _________________________________________

    print('Searching for Cola Can')
    # Starting Camera
    ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')", True)
    # Finding and touching cola can
    ssh.run_channel_command(f"robot.touch_cola()", True)
    sleep(7)
    #  Stopping Camera
    ssh.run_channel_command(f"robot.stop_camera()")

    sleep(1)
    ssh.download_file(f'Videos/{drive_video_file}_{counter}.avi', f'temp/{drive_video_file}_{counter}.avi')
    sleep(1)
    x_curr, y_curr, angle_curr, R, phi, orientation = process_video(f'{drive_video_file}_{counter}', x_curr, y_curr, angle_curr, R, phi, orientation, crop=0.5)
    target_angle, delta = polar_way_back(orientation,phi)

    x_list.append(x_curr_plot)
    y_list.append(y_curr_plot)
    R_list.append(R[0])
    phi_list.append(phi[0])

    counter += 1


    while(R >= 0.2 and counter < 6): 
        print(f'''
        #   x: {x_curr_plot}
        #   y: {y_curr_plot}
          orientation: {orientation}
          phi: {phi}
          Length back: {R}
          Target Angle: {target_angle}
          Delta: {delta}
        ''')
        
        ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')", True)
        sleep(1)
        # Note: Video is mirrored
        if delta < -.1: # tegen de klok in
            ssh.run_channel_command('robot.turn_left()')
        elif delta > .1:
            ssh.run_channel_command('robot.turn_right()')
        else:
            ssh.run_channel_command('robot.drive_forward()') 
        sleep(0.7)
        ssh.run_channel_command('robot.stop()')
        ssh.run_channel_command(f'robot.stop_camera()')
        sleep(1)
        ssh.download_file(f'Videos/{drive_video_file}_{counter}.avi', f'temp/{drive_video_file}_{counter}.avi')

        x_curr, y_curr, angle_curr, R, phi, orientation = process_video(f'{drive_video_file}_{counter}', x_curr, y_curr, angle_curr, R, phi, orientation, crop=0.5)
        target_angle, delta = polar_way_back(orientation,phi)

        x_list.append(x_curr_plot)
        y_list.append(y_curr_plot)
        R_list.append(R[0])
        phi_list.append(phi[0])


        counter += 1
    
    print('Reached orignal location!')

    ssh.run_channel_command(f'quit()')
    ssh.close()

    print(R_list)
    print(phi_list)
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot((np.array(phi_list)*360) / (2*np.pi) , R_list)
    ax.set_aspect('equal')
    plt.show()
    fig.savefig('drive.pdf')
