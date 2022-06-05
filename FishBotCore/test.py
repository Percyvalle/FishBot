import queue
import sys
import threading
import cv2
import keyboard
import mouse
from pynput.mouse import Button, Controller
import queue as qu
import numpy as np

from mss.linux import MSS as mss
import mss

def find_fish():
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

        while "Screen capturing":
            if keyboard.is_pressed('q'):
                return 0

            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            for x in range(7):
                fish = cv2.imread(f'res/fish_{x}.png', cv2.IMREAD_GRAYSCALE)
                res = cv2.matchTemplate(img, fish, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res > 0.8)

                if len(list(zip(*loc[::-1]))) != 0:
                    for pt in zip(*loc[::-1]):
                        if pt[0] >= 920:
                            print('Справа')
                            keyboard.release('d')
                            keyboard.press('a')
                        elif pt[0] < 920:
                            print('Слева')
                            keyboard.release('a')
                            keyboard.press('d')

def find_text():
    mouse = Controller()
    with mss.mss() as sct:
        monitor = {"top": 780, "left": 1120, "width": 800, "height": 300}

        while "Screen capturing":
            if keyboard.is_pressed('q'):
                return 0
            img = np.array(sct.grab(monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            for x in range(4):
                text = cv2.imread(f'res/text_{x}.png', cv2.IMREAD_GRAYSCALE)
                res = cv2.matchTemplate(img, text, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res > 0.7)

                w, h = text.shape[::-1]
                if len(list(zip(*loc[::-1]))) != 0:
                    mouse.press(Button.left)
                else:
                    mouse.release(Button.left)


def hotkey():
    keyboard.press_and_release('e')

    th1 = threading.Thread(target=find_fish)
    th1.start()

    th2 = threading.Thread(target=find_text)
    th2.start()

    th2.join()
    sys.exit()


if __name__ == "__main__":
    while True:
        if keyboard.is_pressed('ctrl+h'):
            hotkey()