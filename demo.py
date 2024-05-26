from lib.LLM import LLM
from lib.SpeechRecognizer import SpeechRecognizer
from lib.SSH import SSH


if __name__ == "__main__":
    ssh = SSH()
    ssh.transfer_file('picarx/make_picture.py', 'Downloads/make_picture.py')
    command = '''
    python3 Downloads/make_picture.py
    '''
    ssh.run_command(command)
    ssh.download_file(outbound_filepath="/home/pi/Pictures/test.jpg", local_filepath='temp/test.jpg')

    