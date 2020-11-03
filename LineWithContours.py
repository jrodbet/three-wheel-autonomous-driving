#import from OpenCV and Python-libraries
import numpy as np
import math
import cv2
#imports from own Files
from PositionsOfLine import PositionsOfLine

"""
Author: Amanda Klingner
Filename: LineWithContours.py
Description: Class for the line detection algorithm with contours
Links for Help:
- https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/ (for region of interest)
- https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html (for find Contours)
- https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/ (for find Contours)
- https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/ (for blue color lines)
- https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html (for black color lines)
- https://techtutorialsx.com/2019/04/13/python-opencv-converting-image-to-black-and-white/ (for black color lines)
"""
class LineDetectionContours:
	#initialise  the height and width for the image
	global height
	global width

	"""
	constructor for LineDetectionContours
	"""
	def __init__(self):
		pass

	"""
	main methode for line detection with contours and used from the main programm
	parameter:
	- frame: the frame (image) of the camera
	return: the object with the 2 postions of the middle line
	"""
	def lineDetectionContours(self,frame):
		#save the height and width of the image
		self.width=frame.shape[1]
		self.height=frame.shape[0]
		#positions for first section of the picture
		xPos1= 0
		yPos1= self.height-20
		wPos1= self.width
		hPos1= 10
		#postions for second section of the picture
		xPos2= 0
		yPos2= int((self.height/2)+60)
		wPos2= self.width
		hPos2= 10
		#positions for third section of the picture
		xPos3= 0
		yPos3= int((self.height/2)+40)
		wPos3= self.width
		hPos3= 20

		#save the regions of the 3 different sections
		regionOfInterest1 = self.getRegionOfInterest(frame,xPos1,yPos1,hPos1,wPos1)
		regionOfInterest2 = self.getRegionOfInterest(frame,xPos2,yPos2,hPos2,wPos2)
		regionOfInterest3= self.getRegionOfInterest(frame,xPos3,yPos3,hPos3,wPos3)
		#get contours of the different sections
		contours1=self.getContours(regionOfInterest1)
		contours2=self.getContours(regionOfInterest2)
		contours3=self.getContours(regionOfInterest3)
		#get the centerpositions of the contours (and highest x and y position for only one center point -> not used) (for the 3 different secetions)
		xyCenters1,xPosHigh1,yPosHigh1=self.getCenterOfContours(frame,contours1,xPos1,yPos1)
		xyCenters2,xPosHigh2,yPosHigh2=self.getCenterOfContours(frame,contours2,xPos2,yPos2)
		xyCenters3,xPosHigh3,yPosHigh3 =self.getCenterOfContours(frame,contours3,xPos3,yPos3)

		#initialise the postions of the middle line
		middleOfLinesX1=None
		middleOfLinesX2=None
		middleOfLinesY1=None
		middleOfLinesY2=None
		#save the half width of the image
		middleWidth=self.width/2

		if len(xyCenters1)==2:#if in first region two center points
			middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPointsInOneSection(xyCenters1[0][0],xyCenters1[0][1],xyCenters1[1][0],xyCenters1[1][1])
		elif len(xyCenters2)==2:#if in second region two center points
			middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPointsInOneSection(xyCenters2[0][0],xyCenters2[0][1],xyCenters2[1][0],xyCenters2[1][1])
		elif len(xyCenters3)==2:#if in third region two center points
			middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPointsInOneSection(xyCenters3[0][0],xyCenters3[0][1],xyCenters3[1][0],xyCenters3[1][1])
		elif len(xyCenters1)==1:#first region one center point
			if len(xyCenters2)==1:#first region one center point and in second region one center ppoint
				print("1.region=1point and 2.region= 1point first")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters1[0][0],xyCenters1[0][1],xyCenters2[0][0],xyCenters2[0][1])
			elif len(xyCenters3)==1:#first region one center point and in third region one center ppoint
				print("1.region=1point and 2.region= 1point first")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters1[0][0],xyCenters1[0][1],xyCenters3[0][0],xyCenters3[0][1])
		elif len(xyCenters2)==1:#second region one center point
			if len(xyCenters1)==1:#second region one center point and in first region one center ppoint
				print("1.region=1point and 2.region= 1point second")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters1[0][0],xyCenters1[0][1],xyCenters2[0][0],xyCenters2[0][1])
			elif len(xyCenters3)==1:#second region one center point and in third region one center ppoint
				print("1.region=1point and 2.region= 1point first")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters3[0][0],xyCenters3[0][1],xyCenters2[0][0],xyCenters2[0][1])
		elif len(xyCenters3)==1:#thrid region one center point
			if len(xyCenters1)==1:#third region one center point and in first region one center ppoint
				print("1.region=1point and 2.region= 1point second")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters3[0][0],xyCenters3[0][1],xyCenters1[0][0],xyCenters1[0][1])
			elif len(xyCenters2)==1:#third region one center point and in second region one center ppoint
				print("1.region=1point and 2.region= 1point first")
				middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2=self.findTwoPoints(xyCenters3[0][0],xyCenters3[0][1],xyCenters2[0][0],xyCenters2[0][1])

		#set the middle line if two postions for the middle line
		if not (middleOfLinesX1 is None) and not (middleOfLinesY1 is None) and not (middleOfLinesX2 is None) and not(middleOfLinesY2 is None):
			cv2.line(frame, (middleOfLinesX1, middleOfLinesY1), (middleOfLinesX2, middleOfLinesY2), (0, 255, 0), thickness=2)
		
		#print the postions of the middle line
		print("posx1: ",middleOfLinesX1)
		print("posx2: ",middleOfLinesX2)
		print("posy1: ",middleOfLinesY1)
		print("posy2: ",middleOfLinesY2)
		#create an objekt with the positions of the middle line
		objPositionsOfLine=PositionsOfLine(middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2,self.height,self.width)
		cv2.imshow('Contours', frame)
		return objPositionsOfLine

	"""
	*** NOT USED ***
	calculate from 4 contours (center points) from two different regions
	parameter:
	- xPos1: first x postion of the first part (1. region or 2.region or 3.region)
	- yPos1: first y postion of the first part (1. region or 2.region or 3.region)
	- xPos2: second x postion of the first part (1. region or 2.region or 3.region)
	- yPos2: second y postion of the first part (1. region or 2.region or 3.region)
	- xPos3: first x postion of the second part (1. region or 2.region or 3.region)
	- yPos3: first y postion of the second part (1. region or 2.region or 3.region)
	- xPos4: second x postion of the second part (1. region or 2.region or 3.region)
	- yPos4: second y postion of the second part (1. region or 2.region or 3.region)
	return: the x and y postions of the middle line (2)
	"""	
	def findFourPoints(self,xPos1,yPos1,xPos2,yPos2,xPos3,yPos3,xPos4,yPos4):
		middleOfLinesX1=int((xPos1+xPos2) / 2)#x middle of the first part
		middleOfLinesY1=int((yPos1+yPos2) / 2)#y middle of the first part
		middleOfLinesX2=int((xPos3+xPos4) / 2)#x middle of the second part
		middleOfLinesY2=int((yPos3+yPos4) / 2)#y middle of the second part
		return (middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2)

	"""
	*** NOT USED ***
	calculate from 3 contours (center points) from two different regions
	parameter:
	- absXPos1: first x postion of the first part (1. region or 2.region or 3.region)
	- absYPos1: first y postion of the first part (1. region or 2.region or 3.region)
	- absXPos2: second x postion of the first part (1. region or 2.region or 3.region)
	- absYPos2: second y postion of the first part (1. region or 2.region or 3.region)
	- xPos3: first x postion of the second part only one position (1. region or 2.region or 3.region)
	- yPos3: first y postion of the second part only one position(1. region or 2.region or 3.region)
	return: the x and y postions of the middle line (2)
	"""	
	def findThreePoints(self,absXPos1,absYPos1,absXPos2,absYPos2,xPos3,yPos3):
		middleOfLinesX2=int((absXPos1+absXPos2) / 2)#x middle of the first part
		middleOfLinesY2=int((absYPos1+absYPos2) / 2)#y middle of the first part
		#initialise the 1.postion of the middle line
		middleOfLinesX1=None
		middleOfLinesY1=None
		#middle of two X in the first part
		absXY=abs(absXPos1-absXPos2)/2
		print("absXPos1",absXPos1)
		print("absXPos1",absXPos2)
		print("absxy",absXY)
		if(yPos3>middleOfLinesY2):#checks if yPos3 higher because yPos3 have on the image the lower Position
			if(middleOfLinesX2>xPos3):#checks if middleOfLinesX2 higher because middleOfLinesX2 have on the image the right Position
				print("right 1: 3.point yPos higher than middleOfLinesY2)")
				middleOfLinesX1=int(xPos3-absXY)#set the 3. point in the middle of the two X from the first part
				middleOfLinesY1=int(yPos3)
			elif (middleOfLinesX2<xPos3):#checks if middleOfLinesX2 smaller because x2 have on the image the left Position
				print("left 1: 3.point yPos higher than middleOfLinesY2)")
				middleOfLinesX1=int(xPos3+absXY)#set the 3. point in the middle of the two X from the first part
				middleOfLinesY1=int(yPos3)
			#else: #checks if the middleOfLinesX2 and the xPos3 equal than take for the middleOfLinesX1 the xPos3
			#	middleOfLinesX1=int(xPos3)
			#	middleOfLinesY1= int(yPos3)
				
		elif(yPos3<middleOfLinesY2):#checks if middleOfLinesY2 higher because middleOfLinesY2 have on the image the lower Position
			if(middleOfLinesX2>xPos3):#checks if xPos3 smaller because xPos3 have on the image the left Position
				print(" left 2: 3.point yPos smaller than middleOfLinesY2)")
				middleOfLinesX1=int(xPos3+absXY)#set the 3. point in the middle of the two X from the first part
				middleOfLinesY1=int(yPos3)
			elif (middleOfLinesX2<xPos3):#checks if xPos3 higher because xPos3 have on the image the right Position
				print(" right 2: 3.point yPos smaller than middleOfLinesY2)")
				middleOfLinesX1=int(xPos3-absXY)#set the 3. point in the middle of the two X from the first part
				middleOfLinesY1=int(yPos3)
			#else:#checks if the middleOfLinesY2 and the xPos3 equal than take for the middleOfLinesX1 the xPos3
			#	middleOfLinesX1=int(xPos3)
			#	middleOfLinesY1= int(yPos3)
		return (middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2)

	"""
	calculate from 2 contours (center points) from one regions
	parameter:
	- xPos1: first x postion of the one part (1. region or 2.region or 3.region)
	- yPos1: first y postion of the one part (1. region or 2.region or 3.region)
	- xPos2: second x postion of the one part (1. region or 2.region or 3.region)
	- yPos2: second y postion of the one part (1. region or 2.region or 3.region)
	return: the x and y postions of the middle line (2)
	"""	
	def findTwoPointsInOneSection(self,xPos1,yPos1,xPos2,yPos2):
		#save the half width of the image
		middleWidth=self.width/2
		middleOfLinesX1=int((xPos1+xPos2) / 2)#x middle of the one part
		middleOfLinesY1=int((yPos1+yPos2) / 2)#y middle of the one part
		middleOfLinesX2=middleWidth#set x the half width at the second point of the middle line
		middleOfLinesY2=self.height#set y the height at the second point of the middle line
		return (middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2)
	
	"""
	calculate from 2 contours (center points) from two different regions
	parameter:
	- xPos1: first x postion of the first part (1. region or 2.region or 3.region)
	- yPos1: first y postion of the first part (1. region or 2.region or 3.region)
	- xPos2: second x postion of the second part (1. region or 2.region or 3.region)
	- yPos2: second y postion of the second part (1. region or 2.region or 3.region)
	return: the x and y postions of the middle line (2)
	"""	
	def findTwoPoints(self,xPos1,yPos1,xPos2,yPos2):
		#initialise the two postions of the middle line
		middleOfLinesX2=None
		middleOfLinesY2=None
		middleOfLinesX1=None
		middleOfLinesY1=None
		#save the half width of the image
		middleWidth=self.width/2
		if not(middleWidth>xPos1) and not(middleWidth>xPos2):#if both positions in the image on the not on the left side
			middleOfLinesX1=int((xPos1+xPos2) / 2)#x middle of the first and second part
			middleOfLinesY1=int((yPos1+yPos2) / 2)#y middle of the first and second part
			middleOfLinesX2=middleWidth
			middleOfLinesY2=self.height
		elif not(middleWidth<xPos1) and not(middleWidth<xPos2):#if both positions in the image on the not on the right side
			middleOfLinesX1=int((xPos1+xPos2) / 2)#x middle of the first and second part
			middleOfLinesY1=int((yPos1+yPos2) / 2)#y middle of the first and second part
			middleOfLinesX2=middleWidth#set x the half width at the second point of the middle line
			middleOfLinesY2=self.height#set y the height at the second point of the middle line
		else:#set the postion
			#set the given posistions as end results
			middleOfLinesX1=xPos1
			middleOfLinesY1=yPos1
			middleOfLinesX2=xPos2
			middleOfLinesY2=yPos2
		return (middleOfLinesX1,middleOfLinesY1,middleOfLinesX2,middleOfLinesY2)

	"""
	find the middle of the contours in one region of interest
	parameter:
	- frame: region of interest of the frame(image) of the camera (frame onle for show the the points)
	- contours: countors from the regions of interest
	- xPos1: x position of begin the region of interest
	- yPos1: y position of begin the region of interest
	return: 
	- xyCenters: array with center points from the contours
	- xPosHigh: the highs x position for one contours (not used)
	- yPosHigh: the highs y position for one contours (not used)
	"""	
	def getCenterOfContours(self,frame,contours,xPos,yPos):
		xyCenters=[]#initialise the array for save the center points of the contours
		for cArray in contours:#run through all contours of the region of interest
			length=len(cArray)
			xPosSmall=float('Inf')#initialise the variable for the small x position 
			xPosHigh=0#initialise the variable for the high x position 
			yPosSmall=float('Inf')#initialise the variable for the small y position 
			yPosHigh=0#initialise the variable for the high y position 
			j=0
			while j<length:
				if xPosSmall>cArray[j][0][0]:#checks the current x postion smaller than the xPosSmall
					xPosSmall=cArray[j][0][0]#set the smaller x position
				if xPosHigh<cArray[j][0][0]:#checks the current x postion higher than the xPosHigh
					xPosHigh=cArray[j][0][0]#set the higher x position
				if yPosSmall>cArray[j][0][1]:#checks the current y postion smaller than the yPosSmall
					yPosSmall=cArray[j][0][1]#set the smaller y position
				if yPosHigh<cArray[j][0][1]:#checks the current y postion higher than the yPosHigh
					yPosHigh=cArray[j][0][1]#set the higher y position
				j=j+1
			cX=int((xPosHigh+xPosSmall) / 2)#calculate the middle from smallest and highest x
			cY = int((yPosHigh+yPosSmall) / 2)#calculate the middle from smallest and highest y
			# draw the contour and center of the shape on the image (only for show in the image)
			cv2.circle(frame, (cX+xPos, cY+yPos), 2, (0, 255, 0), -1)
			#initialise an array for one centerpoint (for one contours)
			oneCenter=[]
			#add x and y position for the current position in the image (Centerpoint of a contour)
			oneCenter.append(cX+xPos)
			oneCenter.append(cY+yPos)
			#add the center point to the list of center points
			xyCenters.append(oneCenter)
		if not(len(xyCenters)==1):#set the high position of x and y to 0 if not have the length of the center points the number 1
			xPosHigh=0
			yPosHigh=0
		return (xyCenters,xPosHigh,yPosHigh)

	"""
	get the region of interes at the point: (yPos1, xPos1) with the dimension full width and same Pixel height (10 or 20 Pixel)
	parameter:
	- frame: the frame (image) from the camera
	- xPos: x position of begin the region of interest
	- yPos: y position of begin the region of interest
	- hPos: height of the region of interest
	- wPos: width of the region of interest
	return: get the region of interes
	Link for Help:
	- https://blog.codecentric.de/2017/06/einfuehrung-in-computer-vision-mit-opencv-und-python/
	"""
	def getRegionOfInterest(self,frame,xPos,yPos,hPos,wPos):
		return frame[yPos:int(yPos+hPos), xPos:int(xPos+wPos)]

	"""
	get the contours of one region of interest
	parameter:
	- frame: region of interest of the frame(image) of the camera
	return: get an array with all contours
	Links for Help:
	- https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html (for find Contours)
	- https://www.pyimagesearch.com/2016/04/11/finding-extreme-points-in-contours-with-opencv/ (for find Contours)
	- https://www.geeksforgeeks.org/detection-specific-colorblue-using-opencv-python/ (for blue color lines)
	- https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html (for black color lines)
	- https://techtutorialsx.com/2019/04/13/python-opencv-converting-image-to-black-and-white/ (for black color lines)
	"""
	def getContours(self,regionOfInterest):
		#blue color lines
		#convert image to a hsv image
		hsvRegion = cv2.cvtColor(regionOfInterest, cv2.COLOR_BGR2HSV)
		kernel = np.ones((15,15),np.float32)/225
		#covert the hsv image with linear filter 2D with the kernel for get better the blue line
		hsv = cv2.filter2D(hsvRegion,-1,kernel)
		
		#lowerBlue = np.array([0,0,0], dtype="uint8")#black test (not so good)
		#upperBlue = np.array([90,90,90], dtype="uint8")#black test (not so good)
		lowerBlue = np.array([70,90,0], dtype="uint8")#lower blue of the range
		upperBlue = np.array([210,255,255], dtype="uint8")#upper blue of the range
		#create a mask for the region of interest with lower and upper range (red or green) 
		#mask white Pixel ist in the lower and upper range and black pixel not in the range
		mask = cv2.inRange(hsv, lowerBlue, upperBlue)

		#find the contours with the mask
		_, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		#draw the contours in the region of interest
		cv2.drawContours(regionOfInterest, contours, -1, (0,255,0), 3)

		#black color lines
		#transform the array to a gray image
		#imgGray = cv2.cvtColor(regionOfInterest , cv2.COLOR_BGR2GRAY)
		#transform the gray color image with gaussian blur algorithem
		#blur = cv2.GaussianBlur(imgGray,(5,5),255)
		#set the tresholds for the image
		#ret, thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
		#find the contours in the threshhold image
		#_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		#draw the contours in the region of interest
		#cv2.drawContours(regionOfInterest, contours, -1, (0,255,0), 3)
		return contours
