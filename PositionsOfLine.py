#import from Python-libraries
import math
"""
Author: Amanda Klingner
Filename: PositionsOfLine.py
Description: Class for save the postions of the virtuell line(beginn (x,y) and end(x,y)) to drive in which course
"""
class PositionsOfLine:
	# global variables for Postion 1 (x,y) and for the Position 2 (x,y)
	global xPos1 
	global xPos2
	global yPos1
	global yPos2
	#global variable for the angle for drive to which course
	global angle
	"""
	constructor for PositionsOfLine
	parameter:
	- xPos1: first x postion of the middle line
	- yPos1: first y postion of the middle line
	- xPos2: second x postion of the middle line
	- yPos2: second y postion of the middle line
	"""
	def __init__(self,xPos1,yPos1,xPos2,yPos2,height,width):
		# set the Postion 1 (x,y) and the Position 2 (x,y)
		self.xPos1=xPos1
		self.xPos2=xPos2
		self.yPos1=yPos1
		self.yPos2=yPos2
		#checks if exist 2 poistions
		if not(self.getXPos1() is None) and not(self.getYPos1() is None) and not(self.getXPos2() is None) and not(self.getYPos2()is None):
			#calculate the angel for drive in which course
			self.angle=self.calculateAngle(xPos1,yPos1,xPos2,yPos2)
		#checks if exist position 1 (x1,y1)
		elif not(self.getXPos1() is None) and not(self.getYPos1() is None):
			#calculate the middle of the picture
			halfWidth=width/2
			#calculate the angle with second Position: the middle of the picture (x2) and the height(y2)
			self.angle=self.calculateAngle(xPos1,yPos1,halfWidth,height)
		#checks if exist position 2 (x2,y2)
		elif not(self.getXPos2() is None) and not(self.getYPos2()is None):
			#calculate the middle of the picture
			halfWidth=width/2
			#calculate the angle with second Position: the middle of the picture (x2) and the height(y2)
			self.angle=self.calculateAngle(xPos2,yPos2,halfWidth,height)
		else:
			self.angle=None
	"""
	get the x position 1
	return: the x position 1
	"""
	def getXPos1(self):
		return self.xPos1

	"""
	get the x position 2
	return: the x position 2
	"""
	def getXPos2(self):
		return self.xPos2

	"""
	get the y position 1
	return: the y position 1
	"""
	def getYPos1(self):
		return self.yPos1

	"""
	get the y position 2
	return: the y position 2
	"""
	def getYPos2(self):
		return self.yPos2

	"""
	get the angle for which course to drive
	return: the angle for which course to drive
	"""
	def getAngle(self):
		return self.angle

	"""
	calculate the angle for which course to drive
	parameter:
	- xPos1: first x postion of the middle line
	- yPos1: first y postion of the middle line
	- xPos2: second x postion of the middle line
	- yPos2: second y postion of the middle line
	return: the angle for which course to drive
	"""
	def calculateAngle(self,posX1,posY1,posX2,posY2):
		angle=None#initialise the variable for the angle
		if posX1==posX2:#checks for set the angle in degree for straightforward
			print("calculate :posX1==posX2 -> straightforward")
			angle=90#set 90 degree for angle in degree straightforward
		elif posY1==posY2:#checks the two y Postion (the height of the Image) on the same level for sharp courses
			if posX1<posX2:#checks for set the angle in degree for sharp left
				print("calculate :posY1==posY2 and posX1<posX2 -> sharp Left")
				angle=180#set 180 degree for angle in degree for sharp left
			elif posX1>posX2:#checks for set the angle in degree for sharp right
				print("calculate :posY1==posY2 and posX1>posX2 -> sharp right")
				angle=0#set 0 degree for angle in degree for sharp right
		elif posY1>posY2:#checks if y1 higher because y1 have on the image the lower Position
			if posX1<posX2:#checks if x2 higher because x2 have on the image the right Position
				print("calculate :posY1>posY2 and posX1<posX2 -> right")
				#calculate the adjacent side (from x1 and x2 (width))
				adjacentSide=float(abs(posX1-posX2))
				#calculate the opposite side (from y1 and y2 (height))
				oppositeSide=float(abs(posY1-posY2))
				divAdjaAndOppo=float(oppositeSide / adjacentSide)
				#calculate the arctangent in radian measure
				angleWithRadian=math.atan(divAdjaAndOppo)
				#transform the radian measure in degree
				angle=int(angleWithRadian * 180.0 / math.pi)
			elif posX1>posX2:#checks if x2 smaller because x2 have on the image the left Position
				print("calculate :posY1>posY2 and posX1>posX2 -> left")
				#calculate the adjacent side (from x1 and x2 (width))
				adjacentSide=float(abs(posX1-posX2))
				#calculate the opposite side (from y1 and y2 (height))
				oppositeSide=float(abs(posY1-posY2))
				divAdjaAndOppo=float(oppositeSide / adjacentSide)
				#calculate the arctangent in radian measure
				angleWithRadian=math.atan(divAdjaAndOppo)
				#transform the radian measure in degree and get the difference of 180 for get a higher angle
				angle=int(180-(angleWithRadian * 180.0 / math.pi))
		elif posY1<posY2:#checks if y2 higher because y2 have on the image the lower Position
			if posX1<posX2:#checks if x1 smaller because x1 have on the image the left Position
				print("calculate :posY1<posY2 and posX1<posX2 -> left")
				#calculate the adjacent side (from x1 and x2 (width))
				adjacentSide=float(abs(posX1-posX2))
				#calculate the opposite side (from y1 and y2 (height))
				oppositeSide=float(abs(posY1-posY2))
				divAdjaAndOppo=float(oppositeSide / adjacentSide)
				#calculate the arctangent in radian measure
				angleWithRadian=math.atan(divAdjaAndOppo)
				#transform the radian measure in degree and get the difference of 180 for get a higher angle
				angle=int(180-(angleWithRadian * 180.0 / math.pi))
			elif posX1>posX2:#checks if x1 higher because x1 have on the image the right Position
				print("calculate :posY1<posY2 and posX1>posX2 -> right")
				#calculate the adjacent side (from x1 and x2 (width))
				adjacentSide=float(abs(posX1-posX2))
				#calculate the opposite side (from y1 and y2 (height))
				oppositeSide=float(abs(posY1-posY2))
				divAdjaAndOppo=float(oppositeSide / adjacentSide)
				#calculate the arctangent in radian measure
				angleWithRadian=math.atan(divAdjaAndOppo)
				#transform the radian measure in degree 
				angle=int(angleWithRadian * 180.0 / math.pi)
		return angle
