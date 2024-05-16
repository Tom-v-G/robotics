from picarx import Picarx
from time import sleep
import readchar
from time import sleep,strftime,localtime
from vilib import Vilib
import os

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
    q: Go to HP
    r: Record video
    e: Stop video
    ctrl+c: Press twice to exit the program
'''

def print_overwrite(msg,  end='', flush=True):
    print('\r\033[2K', end='',flush=True)
    print(msg, end=end, flush=True)


def show_info():
    print("\033[H\033[J",end='')  # clear terminal windows
    print(manual)


if __name__ == "__main__":
    try:
        rec_flag = 'stop' # start,pause,stop
        vname = None
        username = os.getlogin()
        
        Vilib.rec_video_set["path"] = f"/home/{username}/Videos/" # set path

        Vilib.camera_start(vflip=False,hflip=True)
        Vilib.display(local=True,web=True)
        sleep(0.8)  # wait for startup

        pan_angle = -60
        tilt_angle = 15
        px = Picarx()
        
        show_info()
        while True:
            key = readchar.readkey()
            key = key.lower()
            if key in('wsadikjlq'): 
                if 'w' == key:
                    px.set_dir_servo_angle(-8)
                    px.forward(80)
                elif 's' == key:
                    px.set_dir_servo_angle(-7)
                    px.backward(80)
                elif 'a' == key:
                    px.set_dir_servo_angle(-30)
                    px.forward(80)
                elif 'd' == key:
                    px.set_dir_servo_angle(30)
                    px.forward(80)
                elif 'i' == key:
                    tilt_angle+=5
                    if tilt_angle>30:
                       tilt_angle=30
                elif 'k' == key:
                    tilt_angle-=5
                    if tilt_angle<-30:
                        tilt_angle=-30
                elif 'l' == key:
                    pan_angle+=5
                    if pan_angle>30:
                        pan_angle=30
                elif 'j' == key:
                    pan_angle-=5
                    if pan_angle<-100:
                        pan_angle=-100                 
                # go back to home position
                elif 'q' == key:
                    px.set_dir_servo_angle(-7)
                    # turn towards home position
                    # drive forward
                    px.backward(80)

                px.set_cam_tilt_angle(tilt_angle)
                px.set_cam_pan_angle(pan_angle)      
                show_info()                     
                sleep(0.5)
                px.forward(0)
          
            elif key == readchar.key.CTRL_C:
                print("\n Quit")
                break

            # start,pause
            elif key == 'r':
                key = None
                if rec_flag == 'stop':
                    rec_flag = 'start'
                    # set name
                    # vname = strftime("%Y-%m-%d-%H.%M.%S", localtime())
                    vname = "picarx_recording"
                    Vilib.rec_video_set["name"] = vname
                    # start record
                    Vilib.rec_video_run()
                    Vilib.rec_video_start()
                    print_overwrite('rec start ...')
                elif rec_flag == 'start':
                    rec_flag = 'pause'
                    Vilib.rec_video_pause()
                    print_overwrite('pause')
                elif rec_flag == 'pause':
                    rec_flag = 'start'
                    Vilib.rec_video_start()
                    print_overwrite('continue')
            elif key == 'e':
            # stop
                key = None
                rec_flag = 'stop'
                Vilib.rec_video_stop()
                # print_overwrite("The video saved as %s%s.avi"%(Vilib.rec_video_set["path"],vname),end='\n')
                print_overwrite("The video saved as %s%s.avi"%(Vilib.rec_video_set["path"],vname),end='\n')

	    # go back to home position
            #elif key == 'q':
             #   px.set_dir_servo_angle(-7)
              #  px.backward(80)

            # quit
            elif key == readchar.key.CTRL_C:
                print('\nquit')
                break

            # sleep(0.1)

    finally:
        px.set_cam_tilt_angle(15)
        px.set_cam_pan_angle(-60)  
        px.set_dir_servo_angle(0)  
        sleep(.2)


