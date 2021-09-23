from PIL import ImageGrab
import cv2
import numpy as np
import os
from numpy import ones,vstack
from numpy.linalg import lstsq
from statistics import mean
from datetime import datetime

class ImgMenager:
    def __init__(self) -> None:
        self.vertices = np.array([[0, 0] , [450, 0], [580, 250], [580, 600], [150, 600], [0, 400]])
        self.working_dir = os.getcwd()    
    def check_rod(self):
        screen = np.array(ImageGrab.grab(bbox=(700, 150, 1280, 750)))
        processed_img, isline = self.procces_img(screen)
        return screen, processed_img, isline 

    def procces_img(self, org_img):
        processed_img = cv2.Canny(org_img, threshold1=200, threshold2=300)
        processed_img = cv2.GaussianBlur(processed_img, (5,5), 0)  
        processed_img = self.roi(processed_img, [self.vertices])
       
        lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 320, 5)
        if lines is not None:
            lines = [(line[0][0], line[0][1], line[0][2], line[0][3]) for line in lines]
            x1, y1, x2, y2 = self.average_line(lines)
            if not (x1 != x2 and (y2 - y1)/(x2 - x1) > 0):
                # cv2.line(processed_img, (x1, y1), (x2, y2),[255, 255, 255], 3)
                lines = []
        else:
            pass

        return processed_img, bool(lines)

    @staticmethod
    def roi(img, vertices):
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, vertices, 255)
        masked = cv2.bitwise_and(img, mask)
        return masked
    
    def write_img(self, img, *, isfish: bool, **kwargs):
        now = datetime.now()
        formated_date = now.strftime("%d%m%Y_%H%M%S")

        file = f"no_fish_imgs\\no_fish_{formated_date}.jpg"

        if isfish:
            file = f"got_fish_imgs\\got_fish_{formated_date}.jpg"

        cv2.imwrite(f"{self.working_dir}{file}", img)

    def average_line(self, lines):
        try:
            ys = []  
            for x1, y1, x2, y2 in lines:
                ys.extend([y1, y2])

            min_y = min(ys)
            max_y = 600
            new_lines = []
            line_dict = {}

            helper = []
            for idx , xyxy in enumerate(lines):
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m
                if int(x2) >= 150:
                    helper.append((m, b, int(x1), int(x2)))
            

            x2_sum = sum(x2 for m, b, x1, x2 in helper)
            x_mean = x2_sum/len(helper)

            for m, b, x1, x2 in helper:
                if x2 >= x_mean:
                    line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                    new_lines.append([int(x1), min_y, int(x2), max_y])

            final_lanes = {}

            for idx in line_dict:
                final_lanes_copy = final_lanes.copy()
                m = line_dict[idx][0]
                b = line_dict[idx][1]
                line = line_dict[idx][2]
                
                if len(final_lanes) == 0:
                    final_lanes[m] = [ [m,b,line] ]
                    
                else:
                    found_copy = False

                    for other_ms in final_lanes_copy:

                        if not found_copy:
                            if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                                if abs(final_lanes_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_lanes_copy[other_ms][0][1]*0.8):
                                    final_lanes[other_ms].append([m,b,line])
                                    found_copy = True
                                    break
                            else:
                                final_lanes[m] = [ [m,b,line] ]

            line_counter = {}

            for lanes in final_lanes:
                line_counter[lanes] = len(final_lanes[lanes])

            top_lanes = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

            lane1_id = top_lanes[0][0] 

            x1, y1, x2, y2 = self.average_lane(final_lanes[lane1_id])

            assert (x2 > 150 and y2 >= 580) 

            return [x1, y1, x2, y2]
        except:
            return 0, 0, 0, 0

        
    @staticmethod
    def average_lane(lane_data):
        x1_mean = mean(data[2][0] for data in lane_data)
        y1_mean = mean(data[2][1] for data in lane_data)
        x2_mean = mean(data[2][2] for data in lane_data)
        y2_mean = mean(data[2][3] for data in lane_data)
        return int(x1_mean), int(y1_mean), int(x2_mean), int(y2_mean)