Start up file of the Picar-x:

Hotspot:
SSID: robot20
Pwd: robot2020


QuickStart for the PiCar-X Robot

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


## Setting up
1. Create a python virtual environment / conda environtment henceforth refered to as `venv`.
2. Install [portAudio](https://files.portaudio.com/)
3. Install Ollama and in your terminal run the command  `ollama run llama3:latest` to download the latest LLM version.
3. install the packages in requirements.txt with pip in your venv
4. Download the  [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models) and place it in a folder called vosk-models
5. Connect with SSH at least once via your terminal with:
```
ssh pi@10.42.0.1 
```


