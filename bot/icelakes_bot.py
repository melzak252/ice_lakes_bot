import pyautogui
import time
import numpy as np
import cv2

from .img_manager.img_manager import ImgManager
class IceLakesBot:
    def __init__(self, max_time: float = 180, pixels = 50, save_img: bool = False):
        self.img_manager = ImgManager()

        self.save_img = save_img
        self.max_time = max_time
        self.pixels = pixels

        self.monitor_x, self.monitor_y = pyautogui.size()

        self.center_x, self.center_y = self.monitor_x//2, self.monitor_y//2
        
        self.counter = 0
        self.line_in_last_loop = False
 
    def check_starting_rod_pos(self):
        _, _, isline = self.img_manager.check_rod()

        if isline:
            return True

        while not isline:
            pyautogui.press("f")
            time.sleep(5)
            _, _, isline = self.img_manager.check_rod()
        
        return False

    def run(self):
        pyautogui.click(self.center_x, self.center_y)

        if not self.check_starting_rod_pos():
            pyautogui.click(self.center_x, self.center_y)

        start = time.time()

        try:
            self.loop(start)                   
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
        
        pyautogui.click()
    
    def loop(self, start):
        self.pause = True
        glitter = False
        t = 0 
        while t < self.max_time:
            if self.pause:
                screen, processed_img, isline = self.img_manager.check_rod()
                                
                cv2.imshow("window", screen)

                if cv2.waitKey(25) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break                
                
                continue
                
            pyautogui.mouseDown(self.move_x(t), self.move_y(t))

            if round(t) % 30 == 0:
                pyautogui.press("r")
            
            if round(t) % 450 == 0 and not glitter:
                pyautogui.press("t")
                glitter = True
            
            if round(t) % 450:
                glitter = False 
            
            _, processed_img, isline = self.img_manager.check_rod()
                    
            if not isline and not self.line_in_last_loop:
                self.got_fish()
                if self.save_img:
                    self.img_manager.write_img(processed_img, isfish=True)
                continue

            if round(t) % 150 == 0 and isline and self.save_img:
                self.img_manager.write_img(processed_img, isfish=False)
        
            cv2.imshow("window", processed_img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
        
            self.line_in_last_loop = isline
            t = time.time() - start
    
    def move_x(self, t):
        return self.center_x + np.sin(t)*self.pixels
    
    def move_y(self, t):
        return self.center_y + (np.sin(t) ** 2) * self.pixels
    
    def skip(self) -> None:
        self.pause = True
    
    def cont(self) -> None:
        self.pause = False
    
    def got_fish(self):
        self.counter += 1
        pyautogui.press("f")
        print(f"Got {self.counter}. fish")
        time.sleep(5)

        isline_lastloop = False
        isline = False
        
        while not isline:
            _, _, isline = self.img_manager.check_rod()  
            if isline:
                if isline_lastloop:
                    break
                
                isline_lastloop = isline
                continue

            pyautogui.press("f")
            pyautogui.press("r")
            time.sleep(5)
        
        time.sleep(1)
        pyautogui.mouseUp(self.center_x, self.center_y)
        pyautogui.click(self.center_x, self.center_y, duration=0.1)
        pyautogui.mouseDown(self.center_x, self.center_y)
        self.line_in_last_loop = True
        print("Start Fishing Again")


