import sys
import threading
import urllib.request
from datetime import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, pyqtSlot

from PyQt5 import QtWidgets, uic

import random
import cv2
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtCore

import recognizeMultiFace


person={0:'신서유기', 1:'유재석',2:'vietnam3',3:'강호동.jfif',4:'규현',5:'바이든',6:'송민호',7:'안재현',8:'은지원',9:'이수근',10:'카리나',11:'피오'}

form_class = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("end.ui")[0]

#소정
form_class3 = uic.loadUiType("facial_recognition.ui")[0]

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
            #소정 수정
            #widget.setCurrentIndex(widget.currentIndex()==0)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            print(widget.currentIndex())

class UIApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        '''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
        #self.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")

        #이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지
        self.key=0
        pic=person[self.key]

        #이미지 오브젝트 -> 이미지 라벨로 픽셀 표시
        self.obj = QPixmap(pic)
        self.obj= self.obj.scaledToHeight(800)
        self.img_label = QLabel()
        self.img_label.setPixmap(self.obj)
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setStyleSheet("background-color : transparent")

        #file name(image name)
        self.img_name=QLabel()
        self.img_name.setText(pic)
        self.img_name.setFont(QFont("궁서", 50))  # 폰트,크기 조절
        self.img_name.setStyleSheet("Color : red")
        self.img_name.setAlignment(Qt.AlignCenter)


        '''★★★★★★★여기 추가 됐어요!!!!!!★★★★★★★★★★★'''
        #카운트 UI
        self.lcd = QLCDNumber()
        self.lcd.display(self.key)
        self.lcd.setDigitCount(1)
        self.lcd.setFixedWidth(200)
        self.lcd.setFixedHeight(100)
        self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")

        '''★★★★★★★여기 교체해주세요!!!!!!★★★★★★★★★★★'''
        #UI layout
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(self.img_label)
        hbox.addStretch(1)
        hbox.addWidget(self.lcd, 0, Qt.AlignTop)
        #vbox.addWidget(self.img_name)

        self.setLayout(hbox)

        self.setWindowTitle('나영석PD')
        self.move(400,50)

        #self.show()
        self.showMaximized()

    #입력 event 처리
    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            self.key=random.randint(1,len(person.keys())-1)
            pic = person[self.key]
            self.obj = QPixmap(pic)
            self.obj = self.obj.scaledToHeight(800)
            self.img_label.setPixmap(self.obj)
            self.lcd.display(self.key)

            #이미지 명
            self.img_name.setText(pic)
        #실패입력
        if e.key() == Qt.Key_A:
            widget.setCurrentIndex(widget.currentIndex() + 1)
            print(widget.currentIndex())

        #종료상황
        elif e.key()== Qt.Key_Backspace:
            self.close()

# 소정
class FaceRecognition(QMainWindow, form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label = QLabel(self)
        self.img_name = QLabel(self)
        self.label.setStyleSheet("background-color : transparent")
        self.img_name.setStyleSheet("background-color : transparent")

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_A:
            #widget.setCurrentIndex(widget.currentIndex()==0)
            self.recognize()


    def showUser(self, min_score_name):
        self.pixmap = QPixmap(min_score_name + '.png')
        self.label.setGeometry(90, 90, 650, 500)
        self.label.setPixmap(self.pixmap)

        self.img_name.setText(min_score_name + "님 환영합니다!")
        self.img_name.setGeometry(90, 500, 1000, 300)
        self.img_name.setFont(QFont("210 오복상회 R", 50))  # 폰트,크기 조절
        self.img_name.setStyleSheet("Color : brown; background-color : transparent;")
        self.img_name.setAlignment(Qt.AlignCenter)



    def recognize(self):
        models = recognizeMultiFace.trains()

        # 카메라 열기
        cap = cv2.VideoCapture(0)

        while (True):
            # 카메라로 부터 사진 한장 읽기
            ret, frame = cap.read()

            # 얼굴 검출 시도
            image, face = recognizeMultiFace.face_detector(frame)
            try:
                min_score = 999  # 가장 낮은 점수로 예측된 사람의 점수
                min_score_name = ""  # 가장 높은 점수로 예측된 사람의 이름

                # 검출된 사진을 흑백으로 변환
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # 위에서 학습한 모델로 예측시도
                for key, model in models.items():
                    result = model.predict(face)
                    if min_score > result[1]:
                        min_score = result[1]
                        min_score_name = key

                # min_score 신뢰도이고 0에 가까울수록 자신과 같다는 뜻이다.
                if min_score < 500:
                    confidence = int(100 * (1 - (min_score) / 300))
                    # 유사도 화면에 표시
                    display_string = str(confidence) + '% Confidence it is ' + min_score_name
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)
                # 75 보다 크면 동일 인물로 간주해 UnLocked!
                if confidence > 60:
                    #cv2.putText(image, "Unlocked : " + min_score_name, (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1,(0, 255, 0),2)
                    cv2.imshow('Face Cropper', image)
                    #cv2.imwrite(min_score_name + '.png', frame)
                    self.showUser(min_score_name)
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                else:
                    # 75 이하면 타인.. Locked!!!
                    cv2.putText(image, "Unknown", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow('Face Cropper', image)
            except:
                # 얼굴 검출 안됨
                cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                cv2.imshow('Face Cropper', image)
                pass

            if cv2.waitKey(1) == 13:
                 break


##

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # 레이아웃 인스턴스 생성
    Window1 = Intro()
    Window2 = UIApp()
    Window3 = End()

    #소정
    Window4 = FaceRecognition()

    # Widget 추가
    widget.addWidget(Window1)
    widget.addWidget(Window2)
    widget.addWidget(Window3)

    #소정
    widget.addWidget(Window4)

    # 프로그램 화면을 보여주는 코드
    widget.showMaximized()
    print(widget.currentIndex())

    sys.exit(app.exec_())
