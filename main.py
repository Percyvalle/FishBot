import asyncio
from cfg import TextScreenCfg, PyTesseractCfg, CasesCfg, FishScreenCfg
from src.recognition_core.recognition import TextRecognition, FishRecognition
import keyboard

pytesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


async def wait_for_key():
    while True:
        if keyboard.is_pressed('ctrl+k'):
            print("Exit")
            exit(1)
        await asyncio.sleep(0.05)


async def run():
    tr = TextRecognition(
        pytesseract_path=PyTesseractCfg(path=pytesseract_path).PYTESSERACT_PATH,
        monitor_cfg=TextScreenCfg(),
    )
    fr = FishRecognition(
        monitor_cfg=FishScreenCfg()
    )

    text_find = asyncio.create_task(tr.start_text_finder(text_cases=CasesCfg.CASES))
    fish_find = asyncio.create_task(fr.start_fish_finder())
    wait_key = asyncio.create_task(wait_for_key())

    await asyncio.gather(text_find, fish_find, wait_key)


if __name__ == "__main__":
    is_program_started = False
    print("Wait for the start")
    while not is_program_started:
        if keyboard.is_pressed('ctrl+k'):
            is_program_started = True
    asyncio.run(run())
