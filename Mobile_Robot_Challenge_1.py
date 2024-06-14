'''
Automatic Control of Robot via SSH
'''

from lib.SSH import SSH
from lib.FlowAnalyzer import process_video, calc_way_back_live
from time import sleep

import readchar
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
    sleep(1)
    print('Activating Camera')
    counter = 0
    drive_video_file = f'drive'
    ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')")
    
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
        if key in('wsadqklop'): 
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
            sleep(0.5)
            ssh.run_channel_command('robot.stop()')
    print('Stopping camera')
    ssh.run_channel_command('robot.stop_camera()')
    ssh.download_file(f'Videos/{drive_video_file}_{counter}.avi', f'temp/{drive_video_file}_{counter}.avi')
    
    

    x_curr, y_curr, angle_curr = process_video(f'{drive_video_file}_{counter}')
    length_back, target_angle, delta = calc_way_back_live(x_curr, y_curr, angle_curr)

    counter += 1

    x_list = [x_curr]
    y_list = [y_curr]
    plt.ion()
    plt.figure()
    plt.scatter(x_list, y_list)
    plt.pause(1e-5)
    plt.show()

    while(length_back >= 0.2): 
        print(f'''
          x: {x_curr}
          y: {y_curr}
          angle: {angle_curr}
          Length back: {length_back}
          Target Angle: {target_angle}
          Delta: {delta}
        ''')
        
        ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')", True)
        sleep(0.5)
        # Note: Video is mirrored
        if delta < -.1: # tegen de klok in
            ssh.run_channel_command('robot.turn_left()')
        elif delta > .1:
            ssh.run_channel_command('robot.turn_right()')
        else:
            ssh.run_channel_command('robot.drive_forward()') 
        sleep(1.5)
        ssh.run_channel_command('robot.stop()')
        ssh.run_channel_command(f'robot.stop_camera()')
        sleep(0.5)
        ssh.download_file(f'Videos/{drive_video_file}_{counter}.avi', f'temp/{drive_video_file}_{counter}.avi')

        x_curr, y_curr, angle_curr = process_video(f'{drive_video_file}_{counter}', x_curr, y_curr, angle_curr)
        length_back, target_angle, delta = calc_way_back_live(x_curr, y_curr, angle_curr)

        x_list.append(x_curr)
        y_list.append(y_curr)
        
        plt.clf()
        plt.scatter(x_list, y_list)
        plt.pause(1e-5)
        plt.show()

        counter += 1
    
    print('Reached orignal location!')

    ssh.close()
