import time
from lib.LLM import LLM
from lib.SpeechRecognizer import SpeechRecognizer
import tkinter as tk
from time import sleep
from lib.SSH import SSH


if __name__ == '__main__':
    
    ssh = SSH()
    ssh.run_channel_command('cd picar-x/Project')
    ssh.run_channel_command('python3')
    ssh.run_channel_command('from Robot import Robot')
    ssh.run_channel_command('robot = Robot()')
    
    while True:
      sr = SpeechRecognizer()
      llm = LLM()
      question_file_path = 'temp/question.txt'
      answer_file_path = 'temp/answer.txt'
      sr.listen(question_file_path, keyword="please")
      
      llm.answer(question_file_path, answer_file_path)

      with open(answer_file_path, 'r') as file:
          text = file.read()
      print(text)

      ssh.run_channel_command(f'robot.bullfight("{text}")', True)  

      input()