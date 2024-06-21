# Codebase Team Kaasplankje

### wifi hotspot credentials
```
SSID: robot20
Pwd: robot2020
```

### picar-x login credentials
```
userID: pi
password: raspberry
```

## Final Project Setup
1. Create a python virtual environment / conda environtment henceforth refered to as `venv`.
2. (Linux only) Install [portAudio](https://files.portaudio.com/) on your machine
3. Install [Ollama](https://ollama.com/) and in your terminal run the command  `ollama run llama3:latest` to download the latest llama LLM version.
3. Install the following packages:
   ```
   vosk=0.3.45
   langchain=0.2.0
   langchain-community=0.2.0
   paramiko=3.4.0
   pyaudio=0.2.14
   numpy=1.26.4
   matplotlib=3.8.3
   readchar=4.1.0
   opencv-python=4.9.0.80
   ```
4. Download the  [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models). Create a folder called vosk-models in your project workspace and place the model in the folder.
5. Connect with SSH at least once via your terminal with the command
```
ssh pi@10.42.0.1 
```
This stores the ssh credentials so that python has access to them. The conneciton can be closed afterwards.
6. Create a folder named "temp" in your project workspace. Videos from the robot will be downloaded to this directory.

## Mobile Robot Challenge Setup
1. Create a python virtual environment / conda environtment henceforth refered to as `venv`.
2. Install the following packages:
   ```
   paramiko=3.4.0
   numpy=1.26.4
   matplotlib=3.8.3
   readchar=4.1.0
   opencv-python=4.9.0.80
   ```
3. Connect with SSH at least once via your terminal with the command
   ```
   ssh pi@10.42.0.1 
   ```
   This stores the ssh credentials so that python has access to them. The connection can be closed afterwards.

4. Create a folder named "temp" in your project workspace. Videos from the robot will be downloaded to this directory.


## Important Files
### Lib folder
- `SSH.py`: Contains a wrapper class for interacting with the Paramiko SSH client.
Allows for connecting with the robot, transferring files, excecuting bash and
python code on the robot and reading the output
- `FlowAnalyzer.py`: Contains functions for calculating the robots position from
the optical flow of a video and calculating the path back to the origin
- `LLM.py`: Contain wrapper functions for interacting with the local LLM
- `SpeechRecognizer.py`: contains wrapper functions for interacting with the local speech recognition model
### Picar-x folder
- `Robot.py`: Contains the code which is run on the Picar-X
### Root folder
- `Mobile_Robot_Challenge_1.py`: code for the first task of the mobile Robot Challenge
- `Mobile_Robot_Challenge_2.py`: code for the second task of the mobile Robot Challenge
- `Final_Robot_Project.py`: code for the final project 





