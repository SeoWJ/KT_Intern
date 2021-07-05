import sys
import urllib.request
import time

import cv2
import numpy as np
from PIL import Image, ImageOps

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from PyQt5 import QtWidgets, uic
import tensorflow.keras

import random

## Settings
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

ansDict = {0: '사과', 1: '바나나', 2: '포도', 3: '딸기', 4: '레몬', 5: 0} # 해당 퀴즈에서 과일의 종류는 다음과 같습니다.

person={0:'신서유기', 1:'유재석',2:'vietnam3',3:'강호동.jfif',4:'규현',5:'바이든',6:'송민호',7:'안재현',8:'은지원',9:'이수근',10:'카리나',11:'피오'}

form_class = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("miss.ui")[0]

class Intro(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_A:
            widget.setCurrentIndex(widget.currentIndex()+1)
            widget.setStyleSheet(
                "background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")
            print(widget.currentIndex())

class End(QMainWindow, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_A:
            widget.setCurrentIndex(widget.currentIndex()==0)
            print(widget.currentIndex())

class UIApp(QWidget):

    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.label.setStyleSheet("background-color : transparent")
        self.img_name = QLabel(self)
        self.img_name.setStyleSheet("background-color : transparent")
        self.questionNum = 10  # 출제 문제 갯수
        self.randList = self.random_List(self.questionNum, len(ansDict))
        self.ans = ansDict[0]


    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_A:
            #widget.setCurrentIndex(widget.currentIndex()==0)
            self.label.setVisible(False)
            self.quiz()
        if e.key() == Qt.Key_Space:
            self.quizStart(self.ans)
            self.label.setVisible(True)


    ## 문제 출제 (1번 게임 코드 활용)
    def random_List(self, imageNum, maxImageNum):
        result = []

        for v in range(maxImageNum):
            result.append(v)
            random.shuffle(result)

        return result[0:imageNum]

    def makeQuiz(self):
        # global answerList

        answerIndex = self.randList[-1]

        self.ans = ansDict[answerIndex]

        if not self.ans == 0:
            ## 출력 부분 추가 (출력문 or UI) - 현경
            self.img_name.setText(str(self.ans) + ' 를 들고오세요.')
            self.img_name.setGeometry(150, 200, 1000, 300)
            self.img_name.setFont(QFont("210 오복상회 R", 70))  # 폰트,크기 조절
            self.img_name.setStyleSheet("Color : brown; background-color : transparent;")
            self.img_name.setAlignment(Qt.AlignCenter)

        else:
            return 1



    def quizStart(self, ans):
        # 카메라 열기
        cap = cv2.VideoCapture(0)
        print("AAA")

        while (True):
            # 카메라로 부터 사진 한장 읽기
            ret, frame = cap.read()

            # 얼굴 검출 시도

            cv2.imwrite('test.jpg', frame)
            # cv2.imshow('frame_color', frame)
            prediction = self.pred('test.jpg')  # 모델에 추론 이미지 인풋

            # 정답 확인.
            if ansDict[0] == ans and prediction[0][0] >= 0.6:
                # 정답
                # sound.correctSound()
                print('사과 Correct !!')
                cap.release()
                cv2.destroyAllWindows()
                break

            elif ansDict[1] == ans and prediction[0][1] >= 0.6:
                # 정답
                # sound.correctSound()
                print('바나나 Correct !!')
                cap.release()
                cv2.destroyAllWindows()
                break

            elif ansDict[2] == ans and prediction[0][2] >= 0.6:
                # 정답
                # sound.correctSound()
                print('포도 Correct !!')
                cap.release()
                cv2.destroyAllWindows()
                break

            elif ansDict[3] == ans and prediction[0][3] >= 0.6:
                # 정답
                # sound.correctSound()
                print('딸기 Correct !!')
                cap.release()
                cv2.destroyAllWindows()
                break

            elif ansDict[4] == ans and prediction[0][4] >= 0.6:
                # 정답
                # sound.correctSound()
                print('레몬 Correct !!')
                cap.release()
                cv2.destroyAllWindows()
                break
            else:
                continue

        self.pixmap = QPixmap('test.jpg')
        self.label.setGeometry(90, 90, 650, 500)
        self.label.setPixmap(self.pixmap)
        self.img_name.setGeometry(90, 500, 1000, 300)
        self.img_name.setText("맞았습니다!")

    ## (2) 티처블 머신 학습된 모델 코드
    def pred(self, inference_data_path):  # .jpg 타입
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        image = Image.open(inference_data_path)

        # resize the image to a 224x224 with the same strategy as in TM2:
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # display the resized image
        # image.show()

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        # print(prediction) ## 출력 결과 (각 Class별 확률값)pre

        ###prediction = [0, 0, 0.7, 0.3, 0]
        ###print(ans[0])

        return prediction

    def quiz(self):
        count = self.questionNum

        while count > 0:
            self.randList = self.random_List(self.questionNum, len(ansDict))

            self.makeQuiz()  ## makeQuiz() -> 내 quizStart() 작동 -> 그 안에서 정답판별 및 처리하는 구조,,

            count -= 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # 레이아웃 인스턴스 생성
    Window1 = Intro()
    Window2 = UIApp()
    Window3 = End()

    # Widget 추가
    widget.addWidget(Window1)
    widget.addWidget(Window2)
    widget.addWidget(Window3)

    # 프로그램 화면을 보여주는 코드
    widget.showMaximized()
    print(widget.currentIndex())

    sys.exit(app.exec_())