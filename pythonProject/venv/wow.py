from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("test.ui", self)

    def keyPressEvent(self, e):
        # 입력 상황
        if e.key() == Qt.Key_Space:
            widget.setCurrentIndex(widget.currentIndex()-1)

class ScreenCaptureClass(QDialog):

    def __init__(self) :
        super().__init__()
        loadUi("test.ui", self)


    def keyPressEvent(self, e):
        # 입력 상황
        if e.key() == Qt.Key_Space:
            widget.setCurrentIndex(widget.currentIndex()-1)

    def closeEvent(self, event):
        self.deleteLater()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    #레이아웃 인스턴스 생성
    mainWindow = MainWindow()
    captureWindow = ScreenCaptureClass()

    #Widget 추가
    widget.addWidget(mainWindow)
    widget.addWidget(captureWindow)

    #프로그램 화면을 보여주는 코드
    widget.setFixedHeight(275)
    widget.setFixedWidth(390)
    widget.show()
    print(widget.currentIndex())
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()