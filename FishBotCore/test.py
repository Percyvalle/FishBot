import numpy as np
import mss
import cv2
import imutils
import pyautogui


if __name__ == "__main__":
    with mss.mss() as sct:
        # monitor = {"top": 200, "left": 710, "width": 1920, "height": 600}
        monitor = {"top": 150, "left": 0, "width": 1920, "height": 600}

        while "Screen capturing":
            img = np.array(sct.grab(monitor))
            # img = cv2.imread("C:/Users/goman/Desktop/FishBot/FishBotCore/res/fish_find_1.jpg")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            edges = cv2.Canny(gray, 100, 250)


            kernel =  cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
            close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

            cnts = cv2.findContours(close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            total = 0
            for c in cnts:
                p =  cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, p * 0.02, True)
                if len(approx) == 4:
                    cv2.drawContours(img, [approx], -1, (0, 255, 0), 4)
                    total += 1

                    M = cv2.moments(approx)
                    if int(M['m10']) != 0 or int(M['m00']) != 0:
                        cx = int(M['m10']/M['m00'])
                    pyautogui.moveTo(cx, 100)

            cv2.imshow('Name', img)
            if cv2.waitKey(60) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break