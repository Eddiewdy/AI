import cv2
from HandTracking.HandTrackingModule import handDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = handDetector(detectionCon=0.7)
colorR = (255, 0, 255)
colorM = (255, 255, 0)

cx, cy, w, h = 100, 100, 200, 200


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size
        self.color = colorR

    def default(self):
        self.color = colorR

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        # If the index finger tip is in the rectangle region
        if cx - w // 2 < cursor[1] < cx + w // 2 and \
                cy - h // 2 < cursor[2] < cy + h // 2:
            self.posCenter = cursor[1:]
            self.color = colorM
        else:
            self.color = colorR


rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:
        #     cursor = lmList[8]
        #     print(cursor)
        #     if cx - w // 2 < cursor[1] < cx + w // 2 and cy - h // 2 < cursor[2] < cy + h // 2:
        #         cx, cy = cursor[1], cursor[2]
        #         colorR = (255, 255, 0)
        #     else:
        #         colorR = (255, 0, 255)
        # cv2.rectangle(img, (cx - w // 2, cy - h // 2),
        #               (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        if l < 70:
            cursor = lmList[8]  # index finger tip landmark
            # call the update here
            for rect in rectList:
                rect.update(cursor)
        else:
            for rect in rectList:
                rect.default()

    ## Draw solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size
    #     cv2.rectangle(img, (cx - w // 2, cy - h // 2),
    #                   (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
    #     cvzone.cornerRect(img, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    ## Draw Transperency
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        color = rect.color
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                      (cx + w // 2, cy + h // 2), color, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    cv2.imshow("Image", out)
    cv2.waitKey(1)