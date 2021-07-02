import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from PyQt5 import QtWidgets, uic

import random

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