import sys
import time
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLCDNumber, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRunnable, QCoreApplication, QThreadPool, QTimer, QTime
import random



class UIApp(QWidget):


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(
            "background-color: pink;")

        # 이미지 오브젝트 받아옴 (딕셔너리 형태) 초기값은 신서유기8 페이지

        self.obj = QPixmap('img\pose_intro')
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

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        self.count=0

        # UI layout
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.img_label)

        self.setLayout(self.hbox)

        self.setWindowTitle('posing')
        #self.move(400, 50)

        self.show()


    #입력 event 처리
    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:

            #self.obj = QPixmap('img/pose_pic.png')
            #self.obj = self.obj.scaledToHeight(900)
            #self.img_label.setPixmap(self.obj)
            self.img_label.setText("asdasdasdas")

            self.lcd.display(1)
            self.hbox.addWidget(self.lcd, 0, Qt.AlignTop)
            self.repaint()

    def timeout(self):
        sender = self.sender()
        #if id(sender) == id(self.timer):




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = UIApp()
    ax.show()
    sys.exit(app.exec_())