import sys
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class UIApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 배경파트
        backImage = QImage('background.png')
        sImage = backImage.scaled(1500,937)
        pallete = QPalette()
        pallete.setBrush(10, QBrush(backImage))

        obj = QPixmap('smile')

        obj= obj.scaledToHeight(800)
        img_label = QLabel()
        img_label.setPixmap(obj)

        img_name=QLabel('square.png')
        img_name.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(img_label)
        vbox.addWidget(img_name)

        self.setLayout(vbox)
        self.setPalette(pallete)
        self.setWindowTitle('나영석PD')
        self.move(50,50)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = UIApp()
    sys.exit(app.exec_())