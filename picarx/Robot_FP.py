import sys
import os
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/picarx')
#print(Path(__file__).parents[1])


from picarx import Picarx
from time import sleep
import readchar
from time import sleep,strftime,localtime
from vilib import Vilib
#from robot_hat import Pin, Servo

manual = '''
Press keys on keyboard to control PiCar-X!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    q: Go to HP
    ctrl+c: Press twice to exit the program
'''

def print_overwrite(msg,  end='', flush=True):
    print('\r\033[2K', end='',flush=True)
    print(msg, end=end, flush=True)


def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)

class Robot:

    def __init__(self, recording=False, display=False) -> None:

        self.RECORD = recording
        self.DISPLAY = display

        # Default parameters
        self.default_pan_angle = 0
        self.default_tilt_angle = 0
        self.min_pan = -100
        self.max_pan = 30
        self.min_tilt = -30
        self.max_tilt = 30

        self.power = 50
        self.turning_power = 50
        
        self.left_turn_angle = -24.5
        self.right_turn_angle = 18

        # Initiliase robot
        self.px = Picarx()
        
        self.px.set_cam_tilt_angle(self.default_tilt_angle)
        self.px.set_cam_pan_angle(self.default_pan_angle) 

        

    def start_camera(self):
        try:
            self.vname = 'picarx_recording'
            username = os.getlogin()
            
            Vilib.rec_video_set["path"] = f"/home/{username}/Videos/" # set path
            Vilib.rec_video_set["name"] = self.vname

            Vilib.camera_start(vflip=False,hflip=True)
            if self.DISPLAY: Vilib.display(local=True,web=True)
            sleep(0.8)  # wait for startup

            Vilib.rec_video_run()
            Vilib.rec_video_start()

        except:
            raise Exception("Oopsiewoopsie camera is stukkiewukkie")

    def stop_camera(self):
        Vilib.rec_video_stop()
        print("Video saved as %s%s.avi"%(Vilib.rec_video_set["path"],self.vname),end='\n')

    def manual_mode(self):
        
        if self.RECORD:
            self.start_camera()
        
        show_info()

        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadqklop'): 
                if 'w' == key:
                    self.px.set_dir_servo_angle(-8)
                    self.px.forward(self.power)
                elif 's' == key:
                    self.px.set_dir_servo_angle(-7)
                    self.px.backward(self.power)
                elif 'a' == key:
                    self.px.set_dir_servo_angle(self.left_turn_angle)
                    self.px.forward(self.turning_power)
                elif 'd' == key:
                    self.px.set_dir_servo_angle(self.right_turn_angle)
                    self.px.forward(self.turning_power)  
                elif 'k' == key:
                    self.px.set_arm_angle(-75)
                elif 'l' == key:
                    self.px.set_arm_angle(20)
                elif 'o' == key:
                    self.px.set_grab_angle(-75)
                elif 'p' == key:
                    self.px.set_grab_angle(-10)
                elif 'q' == key:
                    break

                sleep(0.5)
                self.px.forward(0)
          
            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

        # Reset servo angle and motors
        self.px.set_dir_servo_angle(-7)
        self.px.forward(0)
        if self.RECORD:
            self.stop_camera()

if __name__== "__main__":
    picar = Robot(True, True)
    print('Press any key to start')
    start = input()
    picar.manual_mode()
    
    #px = Picarx()
    #print(px.servo_pins)
