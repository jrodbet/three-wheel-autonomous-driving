"""
Author: Amanda Klingner
Filename: MainProgram-Contours.py
Description: Programm to run for use the algorithm with Contours
"""
#import from OpenCV and Python-libraries
import cv2
import numpy as np
import time
#import from robot libraries
from mDev import *
#imports from own Files
from findRedOrGreen import RedOrGreen
from LineWithContours import LineDetectionContours
from DriveWay import DriveWay

#setting of the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FPS,40)
camera.set(3,240)
camera.set(4,320)


mdev = mDEV()
#initialise steering of the motors on
mdev.writeReg(mdev.CMD_DIR1,1)
mdev.writeReg(mdev.CMD_DIR2,1)
#initialise the color of light off (no light)
mdev.writeReg(mdev.CMD_IO1,1)
mdev.writeReg(mdev.CMD_IO2,1)
mdev.writeReg(mdev.CMD_IO3,1)
#initialise ther servos for move the camera and move the front wheels
mdev.writeReg(mdev.CMD_SERVO2,1600)#position for left and right of camera
mdev.writeReg(mdev.CMD_SERVO3,1400)#position for up and down of camera
mdev.writeReg(mdev.CMD_SERVO1,1500)#set position of the front wheels

#initialise the class for Stopp and Go (red and green)
finderColor = RedOrGreen()
#initialise the class for move or drive the robot
drive=DriveWay()
#initialise the class for the algorithm with Contours
objLineDetectionContours=LineDetectionContours()
#booblean varaible for finish the programm
running=True
#counter if no found linies
counter=0
while running:
    #get boolean if the camera on and the frame(image) of the camera
    ret,frame = camera.read()
    #checks if the camera on
    if ret:
        #get boolean value True for drive and False for stop drive
        isGo=finderColor.findGreenOrRed(frame)
        if isGo==True:#drive the robot
            #get an object wich have to positions of the virtuell Line(Beginn (x,y) and End (x,y)) to drive 
            objPositionsOfLine=objLineDetectionContours.lineDetectionContours(frame)
            #check that the posistions have values
            if (not (objPositionsOfLine.getXPos1() is None) and not (objPositionsOfLine.getYPos1() is None) or not (objPositionsOfLine.getXPos2() is None) and not(objPositionsOfLine.getYPos2()is None)) and not(objPositionsOfLine.getAngle() is None):
                #drive the robot with the contours algorithm 
                drive.doGoContours(objPositionsOfLine.getAngle())
            elif counter>10:# if found 9 times no positions
                #stop drive the robot
                drive.doStop()
                print("Ende")
                #finished the program (but not used)
                #running=False
                #break
            else:#raise counter if no found linies
                counter=counter+1

            #for close the image windows and break the programm
            if cv2.waitKey(1) & 0xff == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                break 
        else:#stop drive the robot
            drive.doStop()
