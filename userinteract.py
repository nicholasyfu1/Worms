"""

Andrew Huynh
Summer 2018
Behavior Box project


This code is for if the user selects themotaxis or chemotaxis

"""

from time import *
from picamera import PiCamera
import os


capturerate = 5
runtime = 15
expnumber = 59
camera = PiCamera()
savetofile = "/home/pi/Desktop/Exp" + str(expnumber)
while True:
    if not os.path.exists(savetofile):
        os.makedirs(savetofile)
        break
    else: #duplicated file
        savetofile = savetofile + "(1)"
camera.start_preview(fullscreen=False, window=(0,0,1000,1000))
sleep(2)
#frame.tkraise() #raise to front
for i in range(int(runtime/capturerate+1)):
    camera.capture("/home/pi/Desktop/Exp" + str(expnumber) + "/image" + str(i) + ".jpg")
    print("hit %i" % i)
    if i != int(runtime/capturerate):
       	sleep(capturerate)


camera.stop_preview()
