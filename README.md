# Using the Picar-X

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


## QuickStart for the PiCar-X Robot

1) Switch on the robot.

2) Connect to the robot's WLAN hotspot.
   See above for WLAN SSID and password.

3) When connected to the robot's hotspot, use a RealVNC client 
   on your laptop to connect to IP-address 10.42.0.1

4) Login with the following credentials: 
   login name: pi
   password: raspberry

5) Put the robot on the battery charger, such that the wheels 
   are free to turn.

6) Open a terminal on the VNC desktop, and issue the following commands:
   ```cd picar-x/example```
   ```sudo python3 2.keyboard_control.py```

   Use the wasd-keys to control the robot, and CTRL-C to quit

7) See the other examples for camera input, etc.

See also:

https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_keyboard.html
Etc.

And for Calibration of steering, etc.:
https://docs.sunfounder.com/projects/picar-x/en/latest/python/python_calibrate.html


To get videos from the Picar-x to a local computer you open a terminal and use this code:
```sudo scp -r "pi@10.42.0.1:/home/pi/Videos/picarx_recording.avi" ~/Downloads```





