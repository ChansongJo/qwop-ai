from Agent import Agent
import numpy as np
import logging
import time
import pytesseract
import cv2
import mss

class Game:

    def __init__(self):
        self.agent = Agent()

    def start(self):
        self.agent.reload()
        self.agent.start_game()

    def execute_action(self, action):
        for char in action:
            logging.debug(f'Executing action ${char}')
            getattr(self.agent, char)()

    def get_score(self):
        with mss.mss() as sct:
            shot = sct.grab({"top": 148, "left": 90, "width": 21, "height": 15})
            img = np.array(shot)
            score = pytesseract.image_to_string('./assets/score.png')
            #cv2.imshow('window', np.array(img))
            #cv2.waitKey(1)
        return 0 if score == '' else int(score)

    def get_screen_shot(self):
        with mss.mss() as sct:
            shot = sct.grab({"top": 157, "left": 70, "width": 110, "height": 100})
            """
            TODO:
            TEST ONLY GRAYSCALE
            this processing might not be useful since the important data is in the difference between frames
            """
            img = np.array(shot)
            img[:, :, 2] = 0
            img[:, :, 1] = 0
            blueidx = img[:, :, 0] < 24
            notblueidx = img[:, :, 0] >= 24
            img[blueidx] = 255
            img[notblueidx] = 0
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return img

    def get_screen_shot_timed(self):
        with mss.mss() as sct:
            while True:
                start = time.time()
                shot = sct.grab({"top": 157, "left": 70, "width": 110, "height": 100})
                img = np.array(shot)
                img[:, :, 2] = 0
                img[:, :, 1] = 0
                blueidx = img[:, :, 0] < 24
                notblueidx = img[:, :, 0] >= 24
                img[blueidx] = 255
                img[notblueidx] = 0
                img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                cv2.imshow('window', img)
                cv2.waitKey(1)
                print(start-time.time())
        return img