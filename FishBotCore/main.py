import time
from threading import Thread, Event
import cv2
import keyboard
import numpy as np
import mss
from sentence_transformers import SentenceTransformer, util
import pytesseract


# class StoppableThread(Thread):
#
#     def __init__(self, *args, **kwargs):
#         super(StoppableThread, self).__init__(*args, **kwargs)
#         self._stop_event = Event()
#
#     def stop(self):
#         self._stop_event.set()
#
#     def stopped(self):
#         return self._stop_event.is_set()


class FishBot:

    def __init__(self):

        self.tf = self.TextFinder()
        self.ff = self.FishFinder()
        # self.is_program_active = False
        # self.text_finder_thread = None
        # self.fish_finder_thread = None

    # def check_button_pressed(self):
    #     if keyboard.is_pressed('q') and not self.is_program_active:
    #         self.is_program_active = True
    #         self.text_finder_thread = StoppableThread(target=self.tf.start_text_finder())
    #         self.fish_finder_thread = StoppableThread(target=self.ff.start_fish_finder())
    #         self.text_finder_thread.start()
    #         self.fish_finder_thread.start()
    #         print("has started")
    #         time.sleep(1)
    #     if keyboard.is_pressed('q') and self.is_program_active:
    #         self.is_program_active = False
    #         self.text_finder_thread.stop()
    #         self.fish_finder_thread.stop()
    #         print("has stoped")
    #         time.sleep(1)

    class TextFinder:

        def __init__(self):
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.encoded_sentence = self.model.encode(['вытягивайте рыбу'])
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            self.out_size = 128
            self.bottom_text_monitor = {"top": 1080 - 100, "left": 1920 - 300, "width": 300, "height": 100}

        def start_text_finder(self):

            text_screen = self.screen_capture()

            while "Screen capturing":

                text_image = self.window_grabber(screen=text_screen)
                recognized_sentence = self.sentence_recognizer(image=text_image)
                text_similarity = self.sentence_compare(sentence=recognized_sentence)
                print(text_similarity)
                if text_similarity > 0.8:
                    "Press something"

        def window_grabber(self, screen):
            img = np.array(screen.grab(self.bottom_text_monitor))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            cv2.imshow('screen', gray)

            ch = cv2.waitKey(27)
            if ch == 'q':
                cv2.destroyAllWindows()

            return gray

        @staticmethod
        def sentence_recognizer(image):
            sentence = pytesseract.image_to_string(image, lang='rus')
            return sentence

        def sentence_compare(self, sentence):
            encoded_image_sentence = self.model.encode(sentence)
            similarity = util.cos_sim(encoded_image_sentence, self.encoded_sentence)
            similarity = float(str(similarity[0][0]).strip('tensor(').strip(')'))
            return similarity

        @staticmethod
        def screen_capture():
            with mss.mss() as sct:
                return sct

    class FishFinder:

        def __init__(self):

            self.ACTION_LIST = {
                'right': 'a',
                'left': 'd',
            }

            self.fish_monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
            self.is_finder_active = False

            self.previous_action = None

        def start_fish_finder(self):

            text_screen = self.screen_capture()

            while "Screen capturing":

                text_image = self.window_grabber(screen=text_screen)
                recognized_fish = self.find_fish(image=text_image)
                action = self.fish_recognizer(loc=recognized_fish)
                if self.ACTION_LIST.get(action) is not None:
                    if self.previous_action is not None:
                        keyboard.release(self.previous_action)
                    keyboard.press(self.ACTION_LIST.get(action))
                    self.previous_action = self.ACTION_LIST.get(action)
                print(action)

        @staticmethod
        def screen_capture():
            with mss.mss() as sct:
                return sct

        def window_grabber(self, screen):

            img = np.array(screen.grab(self.fish_monitor))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return img

        @staticmethod
        def find_fish(image):

            for x in range(7):
                fish = cv2.imread(f'res/fish_{x}.png', cv2.IMREAD_GRAYSCALE)
                res = cv2.matchTemplate(image, fish, cv2.TM_CCOEFF_NORMED)
                loc = np.where(res > 0.8)
                return loc

        @staticmethod
        def fish_recognizer(loc):

            if len(list(zip(*loc[::-1]))) != 0:
                for pt in zip(*loc[::-1]):
                    if pt[0] >= 920:
                        return 'right'
                    elif pt[0] < 920:
                        return 'left'
            else:
                return None


if __name__ == "__main__":
    fish_bot = FishBot()
    is_program_running = False
    while "Running":
        if keyboard.is_pressed('ctrl+h') and not is_program_running:
            is_program_running = True
            text_finder_thread = Thread(target=fish_bot.tf.start_text_finder)
            text_finder_thread.start()

            fish_finder_thread = Thread(target=fish_bot.ff.start_fish_finder)
            fish_finder_thread.start()


