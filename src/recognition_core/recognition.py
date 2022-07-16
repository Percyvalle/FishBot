import asyncio
from mss.base import MSSBase
from sentence_transformers import SentenceTransformer, util
import pytesseract
import numpy as np
import mss
import cv2
import imutils


class TextRecognition:

    def __init__(self, pytesseract_path: str, monitor_cfg: object, text_cases: list):
        pytesseract.pytesseract.tesseract_cmd = pytesseract_path
        self._model = SentenceTransformer('all-MiniLM-L6-v2')
        self._encoded_cases = self._model.encode(text_cases)
        self._bottom_text_monitor = {"top": monitor_cfg.TOP, "left": monitor_cfg.LEFT,
                                     "width": monitor_cfg.WIDTH, "height": monitor_cfg.HEIGHT}

    async def start_text_finder(self):

        print("Start Searching For Text")

        text_screen = self._screen_capture()

        is_text_found = False
        while "Screen capturing":
            text_image = self._window_grabber(screen=text_screen)
            recognized_sentence = self._sentence_recognizer(image=text_image)
            is_text_correct = self._sentence_compare(sentence=recognized_sentence.lower().strip("\n"))
            if is_text_correct:
                print("Text: 1")
                is_text_found = True
            elif not is_text_correct and is_text_found:
                raise TextFound
            await asyncio.sleep(0.1)

    def _sentence_compare(self, sentence) -> bool:
        encoded_sentence = self._model.encode(sentence)
        all_similarities = util.cos_sim(encoded_sentence, self._encoded_cases)
        for sim in all_similarities[0]:
            temp_sim = float("{:.4f}".format(sim))
            if temp_sim > 0.8:
                return True
        return False

    def _window_grabber(self, screen) -> list:
        img = np.array(screen.grab(self._bottom_text_monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    @staticmethod
    def _sentence_recognizer(image) -> str:
        sentence = pytesseract.image_to_string(image, lang='rus')
        return sentence

    @staticmethod
    def _screen_capture() -> MSSBase:
        with mss.mss() as sct:
            return sct


class FishRecognition:

    def __init__(self, monitor_cfg: object):
        self._search_area = {"top": monitor_cfg.TOP, "left": monitor_cfg.LEFT,
                             "width": monitor_cfg.WIDTH, "height": monitor_cfg.HEIGHT}

        self._lvl_blur_left = 7
        self._lvl_blur_right = 7
        self._canny_lvl_max = 250
        self._canny_lvl_min = 240

    async def start_fish_finder(self) -> bool:

        print("Start Searching For Fish")
        screen = self._screen_capture()

        is_fish_caught = False
        while "Screen capturing":
            img = np.array(screen.grab(self._search_area))
            for c in self._find_contours(img):
                epsilon = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, epsilon * 0.02, True)
                if len(approx) == 4:
                    m = cv2.moments(approx)
                    if int(m['m10']) != 0 or int(m['m00']) != 0:
                        cx = int(m['m10'] / m['m00'])
                        is_fish_caught = True
                        if cx > 960:
                            print("Fish: 1")
                            pass
                        else:
                            print("Fish: 0")
                            pass
                    elif int(m['m10']) != 0 or int(m['m00']) == 0 and is_fish_caught:
                        return True
                elif len(approx) < 4 and is_fish_caught:
                    raise FishCaught
            await asyncio.sleep(0.2)

    @staticmethod
    def _screen_capture() -> MSSBase:
        with mss.mss() as sct:
            return sct

    def _find_contours(self, img) -> list:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self._lvl_blur_left, self._lvl_blur_right), 0)
        edges = cv2.Canny(gray, self._canny_lvl_min, self._canny_lvl_max)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contour = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour = imutils.grab_contours(contour)
        return contour


class FishCaught(Exception):
    pass


class TextFound(Exception):
    pass
