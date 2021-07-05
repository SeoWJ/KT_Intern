import sys
import time
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLCDNumber, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRunnable, QCoreApplication, QThreadPool, QTimer, QTime
import random

from PyQt5 import QtWidgets, uic

subjects = ["자유의 여신상", "고릴라", "축구선수"]

class UIApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(
            "background-color: pink;")

        # 이미지 오브젝트 받아옴 (딕셔너리 형태)
        self.key = 0
        
        obj = QPixmap('img\pose_intro')
        obj = obj.scaledToWidth(1500)
        self.img_label = QLabel()
        self.img_label.setPixmap(obj)
        self.img_label.setStyleSheet("background-color : transparent")
        self.img_label.setAlignment(Qt.AlignCenter)

        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(2)
        self.lcd.setFixedWidth(200)
        self.lcd.setFixedHeight(100)
        self.lcd.setStyleSheet("""QLCDNumber {background-color: red;}""")

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        #self.count=2

        # UI layout
        self.vbox = QVBoxLayout()

        self.hbox = QHBoxLayout()

        self.title = QLabel('title')
        self.title.setFont(QFont('Arial', 50))
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setVisible(False)

        self.desc = QLabel('description')
        self.desc.setFont(QFont('Arial', 50))
        self.desc.setAlignment(Qt.AlignHCenter)
        self.desc.setVisible(False)

        self.vbox.addWidget(self.title)
        self.vbox.addWidget(self.img_label)
        self.vbox.addWidget(self.desc)

        self.hbox.addLayout(self.vbox)
        self.setLayout(self.hbox)

        self.setWindowTitle('posing')
        #self.move(400, 50)

        self.showFullScreen()

    #입력 event 처리
    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            if self.key >= len(subjects):
                self.close()
            self.count = 5
            self.title.setVisible(False)
            txt= subjects[self.key]
            self.img_label.setText(txt)
            self.img_label.setFont(QFont('Arial', 75))

            self.desc.setVisible(True)
            self.desc.setText('포즈를 취해주세요!')
            self.hbox.addWidget(self.lcd, 5, Qt.AlignTop)

            self.timer.start()
            self.repaint()
            

        elif e.key() == Qt.Key_Backspace:
            self.close()
            
    def timeout(self):
        sender = self.sender()
        self.count-=1
        self.lcd.display(self.count)

        if self.count== -1:
            self.timer.stop()
            self.lcd.display(0)

            self.desc.setVisible(False)
            self.title.setVisible(True)
            self.title.setText('정답공개')

            obj = QPixmap('img\pose_answer'+str(self.key)+'.jpg')
            obj = obj.scaledToWidth(1500)
            self.img_label.setPixmap(obj)

            self.repaint()

            time.sleep(4)

            obj = QPixmap('img\pose_pic.png')
            obj = obj.scaledToWidth(1500)
            self.img_label.setPixmap(obj)
            self.title.setText('촬영사진')
            
            self.key += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = UIApp()
    ax.show()
    sys.exit(app.exec_())
