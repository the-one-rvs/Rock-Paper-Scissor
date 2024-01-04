import cv2 as cv
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv.VideoCapture(0) #for webcam 0,1 refrence the first csam connected to computer,and so on...


detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
imgrand = None 
scores = [0,0] #[AI,Player] 
st = 'Error Detecting!'

while True:
    isTrue, img = cap.read()

    cv.flip(img, 1)

    imgBG = cv.imread('E:\Open CV\Project\Rock_Paper_Scissor\Resources\BG.png')
    img1 = cv.imread('E:\Open CV\Project\Rock_Paper_Scissor\Resources\img1.png',cv.IMREAD_UNCHANGED)
    img2 = cv.imread('E:\Open CV\Project\Rock_Paper_Scissor\Resources\img2.png', cv.IMREAD_UNCHANGED)
    img3 = cv.imread('E:\Open CV\Project\Rock_Paper_Scissor\Resources\img3.png', cv.IMREAD_UNCHANGED)

    if img1 is None:
        print("Error loading image 1")

    resized_height = int(0.7 * (imgBG.shape[0]))
    resized_width = int(0.7 * (imgBG.shape[1]))

    img = cv.resize(img, (400,454), interpolation=cv.INTER_CUBIC)

    imgBG = cv.resize(imgBG, (resized_width, resized_height), interpolation=cv.INTER_CUBIC)


    #Find Hand
    hands, img = detector.findHands(img) #with draw

    if startGame :
        playerMove = None
        if stateResult is False:
            timer = time.time() - initialTime
            cv.putText(imgBG,str(int(timer)),(670,420), cv.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

            if timer>3:
                stateResult = True
                timer = 0

                if hands:
                    hand =hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3

                    randomNumber = random.randint(1,3)
                    if randomNumber == 1 :
                        imgrand = img1
                    elif randomNumber == 2:
                        imgrand = img2
                    else :
                        imgrand = img3

                    
                    if imgrand is None:
                        print("Error loading image")
                    imgBG = cvzone.overlayPNG(imgBG, imgrand, (200,300))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                        (playerMove == 3 and randomNumber == 2) :
                        scores[1] += 1
                        st = 'You Won !'
                        cv.putText(imgBG,'You Won !',(580,500), cv.FONT_HERSHEY_PLAIN, 2, (0,255,255), 3)

                    # AI Wins
                    elif (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                        (playerMove == 2 and randomNumber == 3) :
                        scores[0] += 1
                        st = 'You Loose !'
                        cv.putText(imgBG,'You Loose !',(580,500), cv.FONT_HERSHEY_PLAIN, 2, (0,255,255), 3)

                    elif (playerMove == randomNumber):
                        st = '--- Draw ---'
                        cv.putText(imgBG,'--- Draw ---',(580,500), cv.FONT_HERSHEY_PLAIN, 2, (0,255,255), 3)

                    else :
                        st = 'Error Detecting!'



    imgBG[200:654,842:1242] = img

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgrand, (200,300))
        cv.putText(imgBG,st,(580,500), cv.FONT_HERSHEY_PLAIN, 2, (0,255,255), 3)

    cv.putText(imgBG,str(int(scores[0])),(550,420), cv.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 3)
    cv.putText(imgBG,str(int(scores[1])),(790,420), cv.FONT_HERSHEY_SIMPLEX, 2, (255,0,255), 3)


    cv.imshow('ImgBG',imgBG)

    key = cv.waitKey(1);
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

cap.release()
cv.destroyAllWindows()