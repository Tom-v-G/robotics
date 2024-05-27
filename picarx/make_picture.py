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


def main():
    #picar = Robot(True, True)
    # try:
    username = os.getlogin()
    
    picture_path = f"/home/{username}/Pictures/" # set path
    picture_name = "test"

    Vilib.camera_start(vflip=False,hflip=True)
    sleep(0.8)  # wait for startup

    Vilib.take_photo(photo_name=picture_name, path=f"{picture_path}")
    Vilib.camera_close()
    print(f"Picture saved as {picture_name}", end='\n')
    # except:
    # raise Exception("Oopsiewoopsie camera is stukkiewukkie")
    

if __name__== "__main__":

    main()
    
