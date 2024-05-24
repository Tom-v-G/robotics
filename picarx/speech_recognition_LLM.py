from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

import pyaudio
import vosk
import json
import time
from run_file_on_robot import SSH
import tkinter as tk


template_messages = [
    SystemMessage(content='''
                  You are an assistant that interprets commands which are passed on to a robot. 
                  You give answers which consist of two parts: a short response in which you describe what task the robot is going to perform, and a 
                  JSON dictionary that will be given to the robot.It is important that the second part of your answer is a JSON dictionary with the name json_dict. 
                  The dictionary has the following form:
                  dict = {
                    "function": FUNCTION,
                    "color": COLOR
                  }
                  The FUNCTION keyword should be replaced with the function that the user wants you to use. 
                  When asked to drive to an object, FUNCTION should be 'drive_to'. When asked to grab an object, FUNCTION should be 'grab'.
                  COLOR should be the color of the object (as a string) that the user asks you to interact with. 
                  
                  Here is a list of objects and their color:
                    - cola can: red
                    - fanta can: orange
                    - cassis can: purple
                    - pepsi can: grey
                  
                  As an example, if the user asks you: "Drive to the cola can" your response should be:
                  "Certainly, I will drive to the cola can!
                  json_dict = {
                    "function": drive_to,
                    "color": 'red'
                  }"
                  '''),
    # MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{text}"),
]


model = Ollama(model="llama3:latest")
prompt_template = ChatPromptTemplate.from_messages(template_messages)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
#chain = LLMChain(llm=model, prompt=prompt_template, memory=memory)


runnable = (
    {"text": RunnablePassthrough()} | prompt_template | model | StrOutputParser()
)

def listen():
    
    ssh = SSH()
    
    rec = vosk.KaldiRecognizer(model, 16000)

    # Open the microphone stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    
    # Specify the path for the output text file
    output_file_path = "recognized_text.txt"
    
    # Open a text file in write mode using a 'with' block
    with open(output_file_path, "w") as output_file:
        print("Listening for speech. Say 'Terminate' to stop.")
        # Start streaming and recognize speech
        while True:
            data = stream.read(4096)#read in chunks of 4096 bytes
            if rec.AcceptWaveform(data):#accept waveform of input voice
                # Parse the JSON result and get the recognized text
                result = json.loads(rec.Result())
                recognized_text = result['text']
                
                # Write recognized text to the file
                output_file.write(recognized_text + "\n")
                #print(recognized_text)
                
                # Check for the termination keyword
                if "please" in recognized_text.lower():
                    print("Termination keyword detected. Stopping...")
                    break

        # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()
    with open(output_file_path, 'r') as output_file:
        text = output_file.read()
        text = ' '.join(text.rsplit(' ')[:-1]) # remove termination keyword
        answer = runnable.invoke(text)
    
    answer = ' '.join(answer.rsplit('\'')) 
    answer = ' '.join(answer.rsplit('\"')) 
    print('Q: ' + text)
    print('A:' + answer)
    with open('tts.txt', 'w') as file:
        file.write(answer)
    ssh.transfer_file('tts.txt', 'Downloads/tts.txt')
    command = f'''
    sudo python3 Downloads/tts.py
    '''
    output = ssh.run_command(command)
    ssh.close()

def test():
    print('hi')

if __name__ == '__main__':
    model = vosk.Model("/home/tom/Documents/Robotics/robotics/robotics/picarx/vosk-model-en-us-0.22")

    root = tk.Tk()
    root.title('Robot Command Center')
    root.geometry(f"{200}x{200}")

    add_button = tk.Button(root,
                            bg="grey",
                            fg="black",
                            activebackground="red",
                            activeforeground="black", 
                            text='press me', 
                            command=listen)
    add_button.pack(side= "left")

    root.mainloop()