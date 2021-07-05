import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class UIApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # 윈도우 설정
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('select')

        # QButton 위젯 생성
        self.quiz = QPushButton('인물퀴즈', self)
        self.quiz.clicked.connect(self.do_person)
        self.quiz.setGeometry(10, 10, 200, 50)

        self.pose = QPushButton('포즈퀴즈', self)
        self.pose.clicked.connect(self.do_pose)
        self.pose.setGeometry(150, 80, 200, 50)


        # QDialog 설정
        self.dialog = QDialog()

    # 버튼 이벤트 함수
    def do_person(self):
        # 버튼 추가
        btnDialog = QPushButton("인물퀴즈 띄우세요", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('인물퀴즈')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()
    def do_pose(self):
        # 버튼 추가
        btnDialog = QPushButton("포즈퀴즈 띄우세요", self.dialog)
        btnDialog.move(100, 100)
        btnDialog.clicked.connect(self.dialog_close)

        # QDialog 세팅
        self.dialog.setWindowTitle('포즈퀴즈')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(300, 200)
        self.dialog.show()
    # Dialog 닫기 이벤트
    def dialog_close(self):
        self.dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = UIApp()
    mainWindow.show()
    sys.exit(app.exec_())