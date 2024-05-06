'''
QuickStart for the PiCar-X Robot

1) Switch on the robot.

2) Connect to the robot's WLAN hotspot.
   See above for WLAN SSID and password.

3) When connected to the robot's hotspot, use a RealVNC client 
   on your laptop to connect to IP-address 10.42.0.1

4) Login with the following credentials: 
   login name: pi
   password: raspberry

5) Put the robot on the battery charger, such that the wheels 
   are free to turn.

6) Open a terminal on the VNC desktop, and issue the following commands:
   cd picar-x/example
   sudo python3 2.keyboard_control.py

   Use the wasd-keys to control the robot, and CTRL-C to quit

7) See the other examples for camera input, etc.

See also:

https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_keyboard.html
Etc.

And for Calibration of steering, etc.:
https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_calibrate.html
'''

from picarx import Picarx
from time import sleep
import readchar

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    i: Head up
    k: Head down
    j: Turn head left
    l: Turn head right
    ctrl+c: Quit
'''

def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)


if __name__ == "__main__":
    try:
        pan_angle = 0
        tilt_angle = 0
        px = Picarx()
        show_info()
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjl'):
                if 'w' == key:
                    px.set_dir_servo_angle(0)
                    px.forward(80)
                elif 's' == key:
                    px.set_dir_servo_angle(0)
                    px.backward(80)
                elif 'a' == key:
                    px.set_dir_servo_angle(-35)
                    px.forward(80)
                elif 'd' == key:
                    px.set_dir_servo_angle(35)
                    px.forward(80)
                elif 'i' == key:
                    tilt_angle+=5
                    if tilt_angle>35:
                        tilt_angle=35
                elif 'k' == key:
                    tilt_angle-=5
                    if tilt_angle<-35:
                        tilt_angle=-35
                elif 'l' == key:
                    pan_angle+=5
                    if pan_angle>35:
                        pan_angle=35
                elif 'j' == key:
                    pan_angle-=5
                    if pan_angle<-35:
                        pan_angle=-35

                px.set_cam_tilt_angle(tilt_angle)
                px.set_cam_pan_angle(pan_angle)
                show_info()
                sleep(0.5)
                px.forward(0)

            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)
        px.set_dir_servo_angle(0)
        px.stop()
        sleep(.2)

while True:
    key = readchar.readkey()
    key = key.lower()
    if key in('wsadikjl'):
        if 'w' == key:
            pass
        elif 's' == key:
            pass
        elif 'a' == key:
            pass
        elif 'd' == key:
            pass
        elif 'i' == key:
            pass
        elif 'k' == key:
            pass
        elif 'l' == key:
            pass
        elif 'j' == key:
            pass

    elif key == readchar.key.CTRL_C:
        print("\n Quit")
        break
