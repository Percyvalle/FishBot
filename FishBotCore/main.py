import time

import cv2
import numpy as np
import pyautogui as pg
import pytesseract as ts

from mss.linux import MSS as mss
import mss

def find_patt(image, patt, thres):
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (patt_H, patt_W) = patt.shape[:2]
    res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
    sin_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    loc = np.where(res > thres)
    return patt_H, patt_W, zip(*loc[::-1]), min_loc, max_loc

def start():
    with mss.mss() as sct:
        monitor = {"top": 100, "left":100, "width":1920, "height": 1080}

        image_fish = cv2.imread('res/fish.png', 0)
        image_text = cv2.imread('res/catch_fish_text.jpg')
        while "Screen capturing":
            img = np.array(sct.grab(monitor))

            h, w, points, min_loc, max_loc = find_patt(img, image_fish, 0.70)
            if len(list(points)) != 0:
                if max_loc[0] > 960:
                    #pg.press('a')
                    pass
                else:
                    pass
                    #pg.press('d')

if __name__ == '__main__':
    start()

