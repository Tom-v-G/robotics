import time
from lib.LLM import LLM
from lib.SpeechRecognizer import SpeechRecognizer
import tkinter as tk

def button():
    
    sr = SpeechRecognizer()
    llm = LLM()
    question_file_path = 'temp/question.txt'
    answer_file_path = 'temp/answer.txt'
    sr.listen(question_file_path)
    
    llm.answer(question_file_path, answer_file_path)

    with open(answer_file_path, 'r') as file:
        text = file.read()
    print(text)

if __name__ == '__main__':

    root = tk.Tk()
    root.title('Robot Command Center')
    root.geometry(f"{200}x{200}")

    add_button = tk.Button(root,
                            bg="grey",
                            fg="black",
                            activebackground="red",
                            activeforeground="black", 
                            text='press me', 
                            command=button)
    add_button.pack(side= "left")

    root.mainloop()