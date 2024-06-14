'''
Automatic Control of Robot via SSH
'''

from SSH import SSH
from time import sleep
import readchar

if __name__=='__main__':
    ssh = SSH()
    ssh.run_channel_command('cd picar-x/Project')
    ssh.run_channel_command('python3')
    ssh.run_channel_command('from Robot import Robot')
    ssh.run_channel_command('robot = Robot()')

    # Activate Manual Mode
    print('Activating Camera')
    manual_drive_video_file = 'ManualDrive'
    ssh.run_channel_command(f'robot.start_camera({manual_drive_video_file})')
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
    ssh.download_file('Videos/ManualDrive.avi', 'temp/video.avi')

    
    ssh.close()