# Text recognizer cfg


class TextScreenCfg:
    TOP = 1080 - 100
    LEFT = 1920 - 300
    WIDTH = 300
    HEIGHT = 100


class PyTesseractCfg:
    PYTESSERACT_PATH = None

    def __init__(self, path: str):
        self.PYTESSERACT_PATH = path


class CasesCfg:
    CASES = ["вытягивайте рыбу", "ытягивайте рыбу", "ытягивайте рыб",
             "вытягивайте рыб", "вытягивайте ры", "ытягиывайте ры",
             "вытягивайте рыбу\n", "ытягивайте рыбу\n", "ытягивайте рыб\n",
             "вытягивайте рыб\n", "вытягивайте ры\n", "ытягиывайте ры\n",
             ]


class FishScreenCfg:
    TOP = 200
    LEFT = 0
    WIDTH = 1920
    HEIGHT = 800
