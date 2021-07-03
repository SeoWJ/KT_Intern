
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

form_class = uic.loadUiType("intro.ui")[0]
form_class2 = uic.loadUiType("miss.ui")[0]
form_class3 = uic.loadUiType("end.ui")[0]

from test import Ui_Form

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("test.ui",self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            widget.setCurrentIndex(widget.currentIndex()+1)


class WindowClass2(QMainWindow) :
    def __init__(self):
        super().__init__()
        loadUi("miss.ui",self)

    def setUI(self):
        self.setupUI(self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            widget.setCurrentIndex(widget.currentIndex()-1)

class WindowClass(QMainWindow) :
    def __init__(self):
        super().__init__()
        loadUi("intro.ui")

    def setUI(self):
        self.setupUI(self)

    def keyPressEvent(self, e):
        #입력 상황
        if e.key() == Qt.Key_Space:
            widget.setCurrentIndex(widget.currentIndex()+1)

if __name__ == "__main__" :
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # 레이아웃 인스턴스 생성
    abc = Window()
    test = WindowClass2()
    Window = WindowClass()

    # Widget 추가
    widget.addWidget(abc)
    widget.addWidget(Window)
    widget.addWidget(test)

    # 프로그램 화면을 보여주는 코드
    widget.setFixedHeight(800)
    widget.setFixedWidth(1000)
    widget.show()
    print(widget.currentIndex())
    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()