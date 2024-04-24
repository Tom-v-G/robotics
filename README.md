# Using the Jetson Racer

connect the robot to your computer and navigate to `http://192.168.55.1:8888/lab?` in your browser of choice. 
Go to file -> new -> terminal and type

```
sudo nmcli d wifi connect <WIFINAME> password <WIFIPASSWORD>
```

The robot will now show a local IPadress which can be used to connet to the jupyter environment wirelessly. Something like `http://192.168.1.110:8888/lab?`.

Open the notebook you wish to run and select the myEnv kernel.

If you want to add packages to the kernel, navigate to a terminal window and use the command

```
source myEnv/bin/activate
```
to activate the virtual environment.

## Porting the environment to a new Jetson racer
extract myEnv.zip to the home directory of the Jetson racer and add the myEnv kernel with the commands

```
source myEnv/bin/activate
python -m ipykernel install --name myEnv --display-name "Python (myEnv)" --user
```
Note: this might require reinstalling the local camera and racer modules
```
python3 -m pip install jetcam/.
python3 -m pip install jetracer/.
```
If you get an `Could not initialize camera.  Please see error trace.` runtime error, openCV might be missing the gstreamer library. This can be fixed by deinstalling opencv and running the `install-opencv.sh` script (warning: runtime of approx. 1 hour)


https://github.com/NVIDIA/jetson-gpio
https://github.com/NVIDIA-AI-IOT/jetcam/issues/12
https://docs.posit.co/ide/server-pro/user/2023.03.1/jupyter-lab/guide/jupyter-kernel-management.html
https://github.com/jupyterlab/jupyterlab/issues/12977
