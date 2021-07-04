import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        game1 = QPushButton('인물 퀴즈')
        game1.setStyleSheet("color: green;"
                                "background-color: #7FFFD4")


        game2 = QPushButton('포즈 퀴즈')
        game2.setStyleSheet("color: green;"
                                "background-color: #7FFFD4")


        txt = QLabel('게임 설명')
        txt.setAlignment(Qt.AlignCenter)
        txt.setStyleSheet("color: blue;"
                               "background-color: #87CEFA;"
                               "border-style: dashed;"
                               "border-width: 3px;"
                               "border-color: #1E90FF")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(game1)
        hbox.addStretch(3)
        hbox.addWidget(game2)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addWidget(txt)
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.setWindowTitle('choose game')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())