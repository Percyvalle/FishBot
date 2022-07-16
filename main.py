import asyncio
from cfg import TextScreenCfg, PyTesseractCfg, CasesCfg, FishScreenCfg
from src.recognition_core.recognition import TextRecognition, FishRecognition, FishCaught, TextFound
import keyboard

pytesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


async def wait_for_key():
    while True:
        if keyboard.is_pressed('ctrl+k'):
            print("Exit")
            raise KeyboardInterrupt
        await asyncio.sleep(0.05)


async def run():
    tr = TextRecognition(
        pytesseract_path=PyTesseractCfg(path=pytesseract_path).PYTESSERACT_PATH,
        monitor_cfg=TextScreenCfg(),
        text_cases=CasesCfg.CASES
    )
    fr = FishRecognition(
        monitor_cfg=FishScreenCfg()
    )
    while True:
        keyboard.press("E")

        while True:
            fish_task = asyncio.create_task(fr.start_fish_finder())
            wait_key = asyncio.create_task(wait_for_key())
            try:
                await asyncio.gather(fish_task, wait_key)
            except FishCaught:
                break

        while True:
            text_task = asyncio.create_task(tr.start_text_finder())
            wait_key = asyncio.create_task(wait_for_key())
            try:
                await asyncio.gather(text_task, wait_key)
            except TextFound:
                break


def main():
    is_program_started = False
    print("Wait for the start")
    while not is_program_started:
        if keyboard.is_pressed('ctrl+h'):
            is_program_started = True
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        return main()


if __name__ == "__main__":
    main()
