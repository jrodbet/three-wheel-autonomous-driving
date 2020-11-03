#import from OpenCV and Python-libraries
import cv2
import numpy as np
import time
#import from robot libraries
from mDev import *
"""
Author: Amanda Klingner, John Rodriguez
Filename: DriveWay.py
Description: Class for drive the robot on the correct course and stopp tpo drive
"""
class DriveWay:
	"""
	constructor of DriveWay
	"""
	def __init__(self):
		pass

	"""
	transform the angle(in degree) for the range of the Servus(min 1000 and max 2000)
	parameter:
	- angle: angle from the middle line in degree
	return: the transformed angle(in degree) for the range of the Servus(min 1000 and max 2000)
	"""
	def transformAngleForServer(self, angle):
		transformedAngle=(1000/180)*angle+1000
		return transformedAngle

	"""
	stopp the drive of the robot
	"""
	def doStop(self):
		mdev.writeReg(mdev.CMD_PWM1,0)
		mdev.writeReg(mdev.CMD_PWM2,0)
		mdev.writeReg(mdev.CMD_SERVO1,1500)
		print("STOPP DRIVE")

	"""
	drive the robot for the hough transformation algorithm
	parameter:
	- angle: angle from the middle line in degree
	"""
	def doGo(self,angle):
		transformedAngle=self.transformAngleForServer(angle)
		if transformedAngle<=2000 and transformedAngle>=1000:#for stay in the range of the servo
			if transformedAngle>=1550 and transformedAngle<=1450:#for set a lower speed
				mdev.writeReg(mdev.CMD_PWM1,200)
				mdev.writeReg(mdev.CMD_PWM2,200)
			else:#for set a normal speed
				mdev.writeReg(mdev.CMD_PWM1,300)
				mdev.writeReg(mdev.CMD_PWM2,300)
			#set the angle for the course to drive
			mdev.writeReg(mdev.CMD_SERVO1,int(transformedAngle))
			print("GO NOW-Hough")

	"""
	drive the robot for the contours algorithm
	parameter:
	- angle: angle from the middle line in degree
	"""
	def doGoContours(self,angle):
		transformedAngle=self.transformAngleForServer(angle)
		if transformedAngle<=2000 and transformedAngle>=1000:#for stay in the range of the servo
			if transformedAngle>=1550 and transformedAngle<=1450:#for set a lower speed
				mdev.writeReg(mdev.CMD_PWM1,200)
				mdev.writeReg(mdev.CMD_PWM2,200)
			else:#for set a normal speed
				mdev.writeReg(mdev.CMD_PWM1,300)
				mdev.writeReg(mdev.CMD_PWM2,300)
			#set the angle for the course to drive
			mdev.writeReg(mdev.CMD_SERVO1,int(transformedAngle))
			print("GO NOW-Contours")
