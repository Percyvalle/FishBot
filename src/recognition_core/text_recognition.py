import asyncio
from mss.base import MSSBase
import pytesseract
import numpy as np
import mss
import cv2


class TextRecognition:

    def __init__(self, pytesseract_path: str, monitor_cfg: object, text_cases: list):
        pytesseract.pytesseract.tesseract_cmd = pytesseract_path
        self._cases = text_cases
        self._bottom_text_monitor = {"top": monitor_cfg.TOP, "left": monitor_cfg.LEFT,
                                     "width": monitor_cfg.WIDTH, "height": monitor_cfg.HEIGHT}

    async def start_text_finder(self) -> None:

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

    def _sentence_compare(self, sentence: str) -> bool:
        for case in self._cases:
            if sentence.lower() in case:
                return True
        return False

    def _window_grabber(self, screen: MSSBase) -> list:
        img = np.array(screen.grab(self._bottom_text_monitor))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    @staticmethod
    def _sentence_recognizer(image: list) -> str:
        sentence = pytesseract.image_to_string(image, lang='rus', config='--psm 3')
        return sentence

    @staticmethod
    def _screen_capture() -> MSSBase:
        with mss.mss() as sct:
            return sct


class TextFound(Exception):
    pass
