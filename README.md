# CPU_fan
Code to implement a CPU cooler for the Raspberry Pi 3

Project
-------
[Raspberry Pi fan cooler - Hackster.io](https://www.hackster.io/iscapla/raspberry-pi-fan-cooler-86f3f9)

Installation
------------
No extra installed packages are needed to run this program.

Possible configuration
----------------------
Create a config.ini file in this direction. You can change it in the code.
File: 

	/home/pi/Programs/config.ini

Content:
	
	[Fan]
	waitTime_sec: 5
	avg_list_num: 4
	pin: 19
	minTMP: 44
	maxTMP: 48
	[Others]
	verbose: 0

Electronic Schema
-----------------
![alt text](./Fan_Schematic.png)

Run as a system service
-----------------------
Make sure that program.py is executable running:
```
sudo chmod +x program.py
```

Then, create a file with your favourite editor:
```
sudo nano /lib/systemd/system/cpufan.service
```

And add this content:
```text
[Unit]
Description=CPU Fan cooler program
 
[Service]
ExecStart=/home/pi/Programs/CPU_fan/program.py
StandardOutput=null
 
[Install]
WantedBy=multi-user.target
Alias=cpufan.service
```
Save and execute:
```
sudo systemctl enable cpufan.service
sudo systemctl start cpufan.service
```

More info
---------
Send me an email: iscapla@live.com
