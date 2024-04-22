# robotics

connect the robot to your computer and navigate to `http://192.168.55.1:8888/lab?` in your browser of choice. 
Go to file -> new -> terminal and type
```
sudo nmcli d wifi connect <WIFINAME> password <WIFIPASSWORD>
```
The robot will now show a local IPadress which can be used to connet to the jupyter environment wirelessly. Something like `http://192.168.1.110:8888/lab?`.

Open the notebook you wish to run and select the Jetson kernel.

If you want to add packages to the kernel, navigate to a terminal window and use the command
```
conda activate Jetson
```

followed by 
```
conda install PACKAGE_NAME 
```

