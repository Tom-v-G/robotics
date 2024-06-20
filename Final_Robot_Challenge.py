import time
from lib.LLM import LLM
from lib.SpeechRecognizer import SpeechRecognizer
import tkinter as tk
from time import sleep
from lib.SSH import SSH


def clamp_number(num,a,b):
  return max(min(num, max(a, b)), min(a, b))

if __name__ == '__main__':
    
    ssh = SSH()
    ssh.run_channel_command('cd picar-x/Project')
    ssh.run_channel_command('python3')
    ssh.run_channel_command('from Robot import Robot')
    ssh.run_channel_command('robot = Robot()')

    # def button():
    
    sr = SpeechRecognizer()
    llm = LLM()
    question_file_path = 'temp/question.txt'
    answer_file_path = 'temp/answer.txt'
    sr.listen(question_file_path)
    
    llm.answer(question_file_path, answer_file_path)

    with open(answer_file_path, 'r') as file:
        text = file.read()
    print(text)


    ssh.run_channel_command(f'robot.bullfight("{text.lower()}")', True)   
    # # Activate Manual Mode

    # print('Activating Robot')
    # sleep(5)
    # print('Activating Camera')
    # counter = 0
    # drive_video_file = f'drive'
    # ssh.run_channel_command(f"robot.start_camera('{drive_video_file}_{counter}')")
    # sleep(1)
    

    # root = tk.Tk()
    # root.title('Robot Command Center')
    # root.geometry(f"{200}x{200}")

    # add_button = tk.Button(root,
    #                         bg="grey",
    #                         fg="black",
    #                         activebackground="red",
    #                         activeforeground="black", 
    #                         text='press me', 
    #                         command=button)
    # add_button.pack(side= "left")

    # root.mainloop()