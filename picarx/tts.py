from time import sleep
from robot_hat import Music,TTS
import readchar
from os import geteuid

if geteuid() != 0:
    print(f"\033[0;33m{'The program needs to be run using sudo, otherwise there may be no sound.'}\033[0m")

tts = TTS()


def main():
    tts.lang("en-US")

    with open('/home/pi/Downloads/tts.txt', 'r') as file:
        text = file.read()
    # text = text.decode('ascii')
    text = " ".join(text.split('\n'))
    print(text)
    tts.say(text)

if __name__ == "__main__":
    main()
