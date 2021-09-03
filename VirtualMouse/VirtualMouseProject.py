import cv2
import numpy as np
import VirtualMouse.HandTrackingModule as htm
import autopy
import time
##########################
wCam, hCam = 640, 480
frameR = 50
smoothening = 7
##########################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
detector = htm.handDetector(maxHands=1, detectionCon=0.8)
wScr, hScr = autopy.screen.size()
print(wScr, hScr)
while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
    # 2. Get the tip of the index and middle finger
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)
        # 3. Check which fingers are up
        fingers = detector.fingersUp()
        print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only IndexF Finger : Moving
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinate

            x3 = np.interp(int(x1)//5 * 5, (frameR, wCam-frameR), (0, wScr))
            y3 = np.interp(int(y1)//5 * 5, (frameR, hCam-frameR), (0, hScr))
            print(x1, int(x1)//20 * 20)
            # 6. Smooth Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move
            autopy.mouse.move(x3, y3)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # 8. Both Index and middle Finger are up : Click
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            print(length)
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
            # 9. Find distance between fingers
            # 10. Click mouse if short
            # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    # 12. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)

