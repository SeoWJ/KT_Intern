import sys
import time
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLCDNumber, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QRunnable, QCoreApplication, QThreadPool, QTimer, QTime
import random


import requests
import subprocess

from io import StringIO
from PIL import Image

subjects = ["비상구", "자유의여신상", "축구선수"]
subjects_image=["/home/pi/KT_Intern/PoseQuiz/img/answer_exit.jpg","/home/pi/KT_Intern/PoseQuiz/img/answer_freewoman.jpg","/home/pi/KT_Intern/PoseQuiz/img/answer_soccer.jpg"]

quiz_num=1

#이미지 촬영
def takePicture():
    command = "raspistill -t 1 -o photo.jpg"   
    subprocess.call(command, shell = True)

#이미지 용량 축소
def resizeImg():
    file = 'photo.jpg'
    img = Image.open(file)
    img = img.resize((540, 780), Image.ANTIALIAS)
    img.save('photo.jpg', quality=50)

#포즈 유사도 계산 알고리즘
def cal_tan(pos1, pos2):
    if pos1[0] == pos2[0] :
        pos1[0] += 0.01
    return (pos1[1]-pos2[1])/(pos1[0]-pos2[0])

def cal_average(li):
    sum=0
    for i in li:
        sum += i
    return sum / (len(li))

def cal_error(pivot, data, leng):
    err = 0
    for i in range (0,leng):
        err += pivot[i] - data[i]
    return err / leng

#포즈 분석 수행
def analyzePose(self):
    resizeImg() #용량 축소한 이미지 입력
    APP_KEY = 'cc945fdb4b2b7b18448576eeaaedca61'
    IMAGE_URL ='photo.jpg'
    IMAGE_FILE_PATH = 'photo.jpg'
    session = requests.Session()
    session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

    # URL로 이미지 입력시
    response = session.post('https://cv-api.kakaobrain.com/pose', data={'image_url': IMAGE_URL})
    #print(response.status_code, response.json())

    #이미지 파일 불러오기
    with open(IMAGE_FILE_PATH, 'rb') as f:
        response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', f)])
        print('응답코드',response.status_code, response.json())
        
        #player1, player2 포즈 좌표값 저장
        keypoints1=response.json()[0]['keypoints']
        keypoints2=response.json()[1]['keypoints']
        
        pose_data1=[]
        pose_data2=[]

        for i in range(0,len(keypoints1)-2,3):
            pose_data1.append([keypoints1[i],keypoints1[i+1]])
            pose_data2.append([keypoints2[i],keypoints2[i+1]])
        
        print(pose_data1, pose_data2)

    #정답 포즈 좌표값
    exit_pivot = [[299.5312, 123.7031], [311.5848, 122.4844], [289.8884, 110.2969], [317.6116, 140.7656], [273.0134, 117.6094], [307.9688, 268.7344], [221.183, 196.8281], [369.442, 361.3594], [151.2723, 235.8281], [392.3438, 235.8281], [131.9866, 363.7969], [275.4241, 516.1406], [222.3884, 522.2344], [280.2455, 659.9531], [216.3616, 661.1719], [205.5134, 773.2969], [207.9241, 773.2969]]
    freewoman_pivot=[[315.2009, 240.7031], [326.0491, 233.3906],[307.9688, 233.3906], [339.308, 254.1094], [300.7366, 244.3594], [361.0045, 333.3281], [280.2455, 318.7031], [375.4688, 430.8281], [242.8795, 256.5469], [340.5134, 407.6719], [219.9777, 178.5469], [328.4598, 521.0156], [291.0938, 516.1406], [330.8705, 651.4219], [281.4509, 645.3281], [332.0759, 764.7656], [277.8348, 755.0156]]
    soccer_pivot=[[303.1473, 167.5781], [311.5848, 160.2656], [293.5045, 155.3906], [316.4062, 170.0156], [277.8348, 160.2656], [306.7634, 262.6406], [248.9063, 218.7656], [348.9509, 306.5156], [206.7188, 297.9844], [401.9866, 336.9844], [182.6116, 373.5469], [260.9598, 419.8594], [245.2902, 411.3281], [271.808, 521.0156], [281.4509, 521.0156], [239.2634, 762.3281], [320.0223, 717.2344]]
    pose_pivot=[exit_pivot,freewoman_pivot, soccer_pivot]


    #정답 포즈 tan값
    tan_pivot=[]
    
    #player1, player2 tan값
    tan_data1=[]
    tan_data2=[]

    for i in range (0, len(pose_pivot[0])-1):
        print(self.key)
        tan_pivot.append(cal_tan(pose_pivot[self.key-1][i], pose_pivot[self.key-1][i+1]))
        tan_data1.append(cal_tan(pose_data1[i], pose_data1[i+1]))
        tan_data2.append(cal_tan(pose_data2[i], pose_data2[i+1]))


    #오차율 계산
    error1=abs(cal_error(tan_pivot, tan_data1, len(tan_pivot)))
    error2=abs(cal_error(tan_pivot, tan_data2, len(tan_pivot)))

    if error1<error2:
        win='player1'
        lose='player2'
    else:
        win='player2'
        lose='player1'

    print('오차율: ',error1, error2)
    print('win=',win, 'lose=',lose)

    tan_pivot.clear()
    tan_data1.clear()
    tan_data2.clear()

    return error1, error2


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
            self.key += 1
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
            
            #takePicture()
            analyzePose(self)
            result=analyzePose(self)

            self.desc.setVisible(False)
            self.title.setVisible(True)
            self.title.setText('정답공개')

            answer_img=subjects_image[self.key-1]

            obj = QPixmap(answer_img)
            obj = obj.scaledToWidth(1500)
            self.img_label.setPixmap(obj)

            self.repaint()

            time.sleep(4)

            obj = QPixmap('photo.jpg')
            obj = obj.scaledToWidth(1500)
            self.img_label.setPixmap(obj)
            self.title.setText('촬영사진')
            
            #오차율 출력 => 오차율이 작은 경우 : 승/ 오차율이 큰 경우 : 패
            self.title.setText(str(result[0])) #player1 오차율
            self.title.setText(str(result[1])) #player2 오차율

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = UIApp()
    ax.show()
    sys.exit(app.exec_())