#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import subprocess

from io import StringIO
from PIL import Image

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
def analyzePose():
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
    pose_pivot = [[299.5312, 123.7031], [311.5848, 122.4844], [289.8884, 110.2969], [317.6116, 140.7656], [273.0134, 117.6094], [307.9688, 268.7344], [221.183, 196.8281], [369.442, 361.3594], [151.2723, 235.8281], [392.3438, 235.8281], [131.9866, 363.7969], [275.4241, 516.1406], [222.3884, 522.2344], [280.2455, 659.9531], [216.3616, 661.1719], [205.5134, 773.2969], [207.9241, 773.2969]]

    #정답 포즈 tan값
    tan_pivot=[]
    
    #player1, player2 tan값
    tan_data1=[]
    tan_data2=[]

    for i in range (0, len(pose_pivot)-1):
        tan_pivot.append(cal_tan(pose_pivot[i], pose_pivot[i+1]))
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
    
if __name__ == '__main__':
    takePicture()
    analyzePose()
