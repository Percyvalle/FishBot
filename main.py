import asyncio
from cfg import TextScreenCfg, PyTesseractCfg, CasesCfg, FishScreenCfg
from src.recognition_core.recognition import TextRecognition, FishRecognition
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
        text_found = False
        fish_found = False

        while not fish_found:
            fish_task = asyncio.create_task(fr.start_fish_finder())
            wait_key = asyncio.create_task(wait_for_key())
            fish_found = await asyncio.gather(fish_task)
            await asyncio.gather(wait_key)

        while not text_found:
            text_task = asyncio.create_task(tr.start_text_finder())
            wait_key = asyncio.create_task(wait_for_key())
            text_found = await asyncio.gather(text_task)
            await asyncio.gather(wait_key)


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