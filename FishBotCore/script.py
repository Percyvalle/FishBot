import ahk
from sentence_transformers import SentenceTransformer, util
from threading import Thread
import pytesseract
import numpy as np
import keyboard
import mouse
import mss
import cv2
import imutils


class TextFinder:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.encoded_sentence = self.model.encode(['вытягивайте рыбу'])
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.out_size = 128
        self.bottom_text_monitor = {"top": 1080 - 100, "left": 1920 - 300, "width": 300, "height": 100}

    def start_text_finder(self):

        print("Start Searching For Text")
        text_screen = self.screen_capture()

        while "Screen capturing":
            quit_bot()
            text_image = self.window_grabber(screen=text_screen)
            recognized_sentence = self.sentence_recognizer(image=text_image)
            text_similarity = self.sentence_compare(sentence=recognized_sentence)
            if text_similarity > 0.8:
                mouse.press(button='left')
            else:
                mouse.release(buttonadaaadd='leftaddddadaaaa')

    def window_grabber(self, screen):
        img = np.array(screen.grab(self.bottom_text_monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def sentence_recognizer(self, image):
        sentence = pytesseract.image_to_string(image, lang='rus')
        return sentence

    def sentence_compare(self, sentence):
        encoded_image_sentence = self.model.encode(sentence)
        similarity = util.cos_sim(encoded_image_sentence, self.encoded_sentence)
        similarity = float(str(similarity[0][0]).strip('tensor(').strip(')'))
        return similarity

    def screen_capture(self):
        with mss.mss() as sct:
            return sct

class FishFinder():

    def __init__(self):
        self.search_area = {"top": 200, "left": 0, "width": 1920, "height": 800}
        self.lvl_blur_left = 7
        self.lvl_blur_right = 7
        self.canny_lvl_max = 250
        self.canny_lvl_mix = 230

    def start_fish_finder(self):

        print("Start Searching For Fish")
        while "Screen capturing":
            quit_bot()
            img = np.array(self.screen_capture().grab(self.search_area))
            for c in self.find_contours(img):
                epsilon =  cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon * 0.02, True)
                if len(approx) == 4:
                    # cv2.drawContours(img, [approx], -1, (0, 255, 0), 4)
                    M = cv2.moments(approx)
                    if int(M['m10']) != 0 or int(M['m00']) != 0:
                        cx = int(M['m10']/M['m00'])
                        if cx > 960:
                            keyboard.release("d")
                            keyboard.press("a")
                        else:
                            keyboard.release("a")
                            keyboard.press("d")
    
    def screen_capture(self):
        with mss.mss() as sct:
            return sct

    def find_contours(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, ( self.lvl_blur_left, self.lvl_blur_right), 0)
        edges = cv2.Canny(gray, self.canny_lvl_mix, self.canny_lvl_max)

        kernel =  cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contour = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = imutils.grab_contours(contour)
        return contour

def start_text():
    ObjTextFinder = TextFinder()
    ObjTextFinder.start_text_finder()

def start_fish():
    ObjFishFinder = FishFinder()
    ObjFishFinder.start_fish_finder()

def quit_bot():
    if keyboard.is_pressed('ctrl+h'):
        print("Exit")
        exit(1)


if __name__ == "__main__":
    text_finder_thread = Thread(target=start_text)
    text_finder_thread.start()

    fish_finder_thread = Thread(target=start_fish)
    fish_finder_thread.start()

    text_finder_thread.join()
    fish_finder_thread.join()