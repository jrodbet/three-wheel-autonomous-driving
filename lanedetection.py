import cv2
import numpy as np
import math
from PositionsOfLine import PositionsOfLine

class laneDetection:
    
    def __init__(self):
        pass

    # Convert all the frames into HSV color space and filter noise
    def hsv_convertion(self, img):
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        kernel = np.ones((15,15),np.float32)/225
        hsv = cv2.filter2D(img_hsv,-1,kernel)
        return hsv

    # Detect the areas of blue on each frame to detect the borders
    def find_borders(self, img):
        lower_blue = np.array([90, 70, 50], dtype ="uint8")      
        upper_blue = np.array([210, 255, 255], dtype="uint8")
        mask = cv2.inRange(img,lower_blue,upper_blue)
        return mask

    # Crop the frames to obtain the region of interest
    def region_of_interest(self, borders):
        height, width = borders.shape
        roi = np.array([[
                (0, height),
                (0 , height * 0.6),
                #(width * 0.3, height * 0.7),
                #(width * 0.7, height * 0.7),
                (width, height * 0.6),
                (width, height)
            ]], np.int32)
        
        mask = np.zeros_like(borders)
        match_mask_color = 255
        cv2.fillPoly(mask, roi, match_mask_color)
        mask_img = cv2.bitwise_and(borders, mask)
        return mask_img

    # Detect the borders with the Hough Transformation
    def detect_border_lines(self, img):
        lane = cv2.HoughLinesP(img,
                                rho=1,
                                theta=np.pi/180, #180
                                threshold=60,   #10
                                lines=np.array([]), 
                                minLineLength=1,    #5
                                maxLineGap=20)   #0
        return lane

    # Detect the slop and intercept of the line equation to detect the side of the
    #  border line, that will be considered to detect the midline
    def average_slop_intercept(self, img, line_segments):
        lane_lines = []

        if line_segments is None:
            print("no line segment detected!")
            return lane_lines

        height, width,_ = img.shape
        left_fit = []
        right_fit = []
        boundary = 1 / 3

        left_region_boundary = width * (1 - boundary)
        right_region_boundary = width *  boundary

        for line_segment in line_segments:
            for x1, y1, x2, y2 in line_segment:
                if x1 == x2:
                    print("skipping vertical lines (slope = infinity)")
                    continue

                fit = np.polyfit((x1, x2), (y1, y2), 1)
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - (slope * x1)

                if slope < 0:
                    if x1 < left_region_boundary and x2 < left_region_boundary:
                        left_fit.append((slope, intercept))
                else:
                    if x1 > right_region_boundary and x2 > right_region_boundary:
                        right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        if len(left_fit) > 0:
            lane_lines.append(self.make_points(img, left_fit_average))

        right_fit_average = np.average(right_fit, axis=0)
        if len(right_fit) > 0:
            lane_lines.append(self.make_points(img, right_fit_average))
            
        print(lane_lines)
        return lane_lines

    #  Auxiliar function to detect the points of the lines
    def make_points(self, img, line):
        height, width, _ = img.shape
        slope, intercept = line
        y1 = height
        y2 = int(y1 / 2)

        if slope == 0:
            slope = 0.1

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        return [[x1, y1, x2, y2]]

    # Display the lines of the borders on each frame of the streaming
    def display_lines(self, frame, lines, line_color=(0, 255, 0), line_width=7): # line color (B,G,R)
        line_image = np.zeros_like(frame)

        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)

        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image

    # Find and return the points of the midline between the borders lines, for each situation,
    # when none, one or two border lines were detected
    def get_midline(self, img, lane_lines):
        height, width,_ = img.shape
        mid = int(width / 2)

        if len(lane_lines) == 2:
            left_x1, _, left_x2, _ = lane_lines[0][0]
            right_x1, _, right_x2, _ = lane_lines[1][0]
            x_offset = ((left_x2 + right_x2)/ 2) - mid
            y_offset = int(height / 2)
            print(mid, x_offset, y_offset)
            print("two lines founded!!!")

        elif len(lane_lines) == 1:
            x1, _, x2, _ = lane_lines[0][0]
            if(x2 - x1) < 0:
                x_offset = x2 - x1
            else:
                x_offset = x2 - x1
            y_offset = int(height / 2)

        elif len(lane_lines) == 0:
            x_offset = None
            y_offset = None

        if not (x_offset is None) and not (y_offset is None):
            x1 = width / 2
            y1 = height
            x2 = x_offset + mid
            y2 = height / 2            
        else:
            x1 = None
            y1 = None
            x2 = None
            y2 = None
        
        midline = [x1, y1, x2, y2]
        
        return midline

    # Add the obtained midline into each frame of the streaming
    def display_heading_line(self, frame, midline, line_color=(0, 0, 255), line_width=8 ):
        heading_image = np.zeros_like(frame)
        height, width, _ = frame.shape
        
        x1 = midline[0]
        y1 = midline[1]
        x2 = midline[2]
        y2 = midline[3]

        if x1 == None :
            cv2.line(heading_image, (0, 0), (0, 0), line_color, line_width)
            heading_image = cv2.addWeighted(frame, 0.9, heading_image, 1, 1)
        else:
            cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
            heading_image = cv2.addWeighted(frame, 0.9, heading_image, 1, 1)

        return heading_image


    # Calls all the functions to find the midline and return the points of midline, height and width of frames
    def houghLaneDetection(self, img):
        height, width, _ = img.shape
        img_hsv = self.hsv_convertion(img)
        borders = self.find_borders(img_hsv)
        cropped_img = self.region_of_interest(borders)
        lane = self.detect_border_lines(cropped_img)
        lane_lines = self.average_slop_intercept(img, lane)
        img_with_lines = self.display_lines(img, lane_lines)
        midline = self.get_midline(img, lane_lines)
        front_img = self.display_heading_line(img_with_lines, midline)
        
        
        points_of_line = PositionsOfLine(midline[0], midline[1], midline[2], midline[3], height, width)

        cv2.imshow('canny', cropped_img)
        cv2.imshow('lines with midline', front_img)
        return points_of_line
