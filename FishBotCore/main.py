import time

import cv2
import numpy as np
import pyautogui as pg
import pytesseract
import keyboard as kb

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
        monitor = {"top": 100, "left":100, "width":500, "height": 500}

        image_fish = cv2.imread('res/fish.png', 0)

        while "Screen capturing":
            img = np.array(sct.grab(monitor))

            h, w, points, min_loc, max_loc = find_patt(img, image_fish, 0.50)
            if len(list(points)) != 0:
                if max_loc[0] > 960:
                    print("Справа")
                    #kb.press('a')
                else:
                    print("Слева")
                    #kb.press('d')

            # h2, w2, points2, min_loc2, max_loc2 = find_patt(img, image_text, 0.70)
            # print(min_loc2)
            # if len(list(points2)) != 0:
            #     if max_loc2[0] > 960:
            #         #pg.press('a')
            #         print("Справа")
            #     else:
            #         #pg.press('d')
            #         print("Слева")

if __name__ == '__main__':
    start()

