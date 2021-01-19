# Smart_Peephole

<p align="center">
    <img src="server/static/img/logo.svg" alt="Logo" width="800">
    <h3 align="center"><strong>Smart Peephole</strong></h3>

<p align="center">
        <strong>Electronic door peephole running on Raspberry Pi, based on Flask framework. Through this web application, you can check who is at your door at any time.</strong>
        <br />
    </p>
</p>

<br />
<br />
<p align="center">
    <img src="images/goingOut.gif" alt="" height="450">
    <p align="center">
        See who's on the staircase!
    </p>
</p>
<br />
<br />

<p align="center">
    <img src="images/faceDetection.gif" alt="" height="450">
    <p align="center">
        Find the face of whoever stands in front of the door ... if you have a problem with that!
    </p>
</p>
<br />
<br />

# Getting started
## Prerequisites
Make sure that you have the following:
* Raspberry Pi
* Camera module
* Micro SD card with Pi OS on it
* Installed Python3 Virtual Environments

<br />
I have used Raspberry Pi 4B 4GB, but Pi 3B should also work fine. Similar with the camera, yout can experiment with different models. I have used ArduCam OV5647 5Mpx with LS-40180 Fish Eye CS mount.
<br />
<br />

## Installing
Before doing anything please remember to change startup script (run.sh). Change `xxx.xxx.x.xxx:xxxx` to your raspberry ip address. You can find it via `ifconfig`. 

1. Install Python3 Virtual Environments (sudo pip3 install virtualenv)
1. Clone repo somewhere on your Pi.
2. Move into repo. (cd Smart_Peephole/)
3. Create virtual environment. (python3 -m venv server/env)
4. Activate virtual environment. (source server/env/activate)
5. Install needed python modules. (pip install -r requirements.txt)
6. Deactivate virtual environment. Won't need it anymore. (deactivate)
7. Make run script exacutable. (chmod +x run.sh)

## Starting
Startup script already contains 


<br />
It is also possible to run this app at startup of Pi. It can be done by modifying .bashrc file. Put the startup script call at the bottom of the mentioned file: run.sh
<br />
<br />

# Build with
* <a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a>
* <a href="https://opencv.org/">OpenCV</a>
* <a href="https://www.sqlite.org/index.html">SQLite</a>
