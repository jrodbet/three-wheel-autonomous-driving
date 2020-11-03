#import from OpenCV and Python-libraries
import cv2
import numpy as np

"""
Author: Amanda Klingner
Filename: FindRedOrGreen.py
Description: Class for check if show red (for stopp) or show green (for dirve (Go))
Links for Help:
- https://tutorials-raspberrypi.de/farberkennung-in-bildern-am-raspberry-pi-mittels-opencv/ 
"""
class RedOrGreen:
    #initialise  the height and width for the image
    global height
    global width
    #boolean vairable for check is show green or red 
    global isGreen

    """
	constructor for RedOrGreen
	"""
    def __init__(self):
        self.isGreen = False#first time is red
    
    """
	set the boolean vairable for check is green or red
    parameter:
	- isGreen: set the boolean vairable for check is green or red
	"""
    def setIsGreen(self,isGreen):
        self.isGreen=isGreen

    """
	get the vairable for check is green or red
    return: True for green and False for red
	"""
    def getIsGreen(self):
        return self.isGreen

    """
	checks if change to red or green
    parameter:
    - image: the frame from the camera
    return: True for green and False for red
    Link for Help:
    - https://tutorials-raspberrypi.de/farberkennung-in-bildern-am-raspberry-pi-mittels-opencv/ 
	"""
    def findGreenOrRed(self,image):
        #set the height and width of the given image
        self.width=image.shape[1]
        self.height=image.shape[0]
        #start position for begin the squard region of 10x10 pixel
        xPos= int((self.height / 2)-5)
        yPos= int((self.width / 2)-5)
        wPos= 10
        hPos= 10

        # start the region of interes at the point: (yPos1, xPos1) with the dimension 10 Pixel width and 10 Pixel height
        regionOfInterest = image[yPos:yPos+hPos, xPos:xPos+wPos]
        #ranges for red and green
        ranges = {
            #range lower and upper red
            "red": ([10, 10, 128], [100, 100, 250]),  # B G R
            #range lower and upper green
            "green": ([10, 100, 10], [120, 220, 90]),  # B G R
        }

        # checks the ranges ones red and ones green
        for key in ranges.keys():
            #save lower range of red or green
            lowerRange = np.array(ranges[key][0], dtype="uint8")
            #save upper range of red or green
            upperRange = np.array(ranges[key][1], dtype="uint8")

            #create a mask for the region of interest with lower and upper range (red or green) 
            #mask white Pixel ist in the lower and upper range and black pixel not in the range
            mask = cv2.inRange(regionOfInterest, lowerRange, upperRange)
            #transform the mask into bits
            output = cv2.bitwise_and(regionOfInterest, regionOfInterest, mask=mask)
            #count the matches how much pixel white
            countMatches=0
            i=0
            while i<len(mask):
                j=0
                while j<len(mask[0]):
                    if mask[i][j]==255:#if the pixel white
                        countMatches=countMatches+1
                    j=j+1
                i=i+1
            if countMatches>70:# if more than 70 pixel white
                if key=="red":# if find red in the region of interest
                    self.setIsGreen(False)# for stop to drive
                    print("***DO STOP***")
                if key=="green":# if find green in the region of interest
                    self.setIsGreen(True)# for do drive
                    print("*** GO ***")
        return self.getIsGreen()


