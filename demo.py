from lib.LLM import LLM
# from lib.SpeechRecognizer import SpeechRecognizer
from lib.SSH import SSH
from ultralytics import YOLO
import matplotlib

matplotlib.use('TkAgg')



if __name__ == "__main__":
    # ssh = SSH()
    # ssh.transfer_file('picarx/make_picture.py', 'Downloads/make_picture.py')
    # command = '''
    # python3 Downloads/make_picture.py
    # '''
    # print('Running command')
    # ssh.run_command(command)
    # print('Downloading Picture')
    # ssh.download_file(outbound_filepath="Pictures/test.jpg", local_filepath='temp/test.jpg')
    # print('Download Complete')
    # model = YOLO("object_detection/container_detect.pt")
    # results = model("temp/test.jpg",show=True,conf=0.8)
    print(results)
    # input()
    
