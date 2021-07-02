import sys
import time
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLCDNumber, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRunnable, QCoreApplication, QThreadPool
import random

from PyQt5.uic.properties import QtGui

person={0:'신서유기', 1:'유재석',2:'vietnam3',3:'강호동.jfif',4:'규현',5:'바이든',6:'송민호',7:'안재현',8:'은지원',9:'이수근',10:'카리나',11:'피오'}
Evnt={0:'Start', 1:'Descript', 2:'Descript_detail', 3:'END'}

class UIApp(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(
            "background-color: qradialgradient(spread:pad, cx:0.499, cy:0.499318, radius:0.871, fx:0.5, fy:0.5, stop:0.0097561 rgba(255, 255, 255, 255), stop:0.887805 rgba(255, 211, 38, 255));")

        # 이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지
        self.key = 0
        start = Evnt[self.key]
        pic = 'event/' + start

        self.obj = QPixmap(pic)
        self.obj = self.obj.scaledToWidth(1500)
        self.img_label = QLabel()
        self.img_label.setPixmap(self.obj)
        self.img_label.setStyleSheet("background-color : transparent")
        self.img_label.setAlignment(Qt.AlignCenter)

        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(1)
        self.lcd.setFixedWidth(200)
        self.lcd.setFixedHeight(100)
        self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")

        # UI layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.img_label)
        # vbox.addWidget(self.img_name)

        self.setLayout(self.hbox)

        self.setWindowTitle('나영석PD')
        self.move(400, 50)

        self.showFullScreen()


    #입력 event 처리
    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            self.key=random.randint(1,len(person.keys())-1)
            name = person[self.key]
            pic = 'images/' + name

            self.obj = QPixmap(pic)
            self.obj = self.obj.scaledToHeight(900)
            self.img_label.setPixmap(self.obj)

            self.lcd.display(self.key)
            self.hbox.addWidget(self.lcd, 0, Qt.AlignTop)
            self.repaint()

        elif e.key()== Qt.Key_A :
            self.key += 1
            self.key=self.key%(len(Evnt.keys())-1)
            start = Evnt[self.key]
            pic = 'event/' + start

            self.obj = QPixmap(pic)
            self.obj = self.obj.scaledToHeight(1000)
            self.img_label.setPixmap(self.obj)

        #종료상황
        elif e.key()== Qt.Key_Backspace:
            start = Evnt[3]
            pic = 'event/' + start

            self.obj = QPixmap(pic)
            self.obj = self.obj.scaledToHeight(1000)
            self.img_label.setPixmap(self.obj)
            self.repaint()
            time.sleep(2)
            self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = UIApp()
    ax.show()
    sys.exit(app.exec_())