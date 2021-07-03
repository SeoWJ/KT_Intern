import requests

from io import StringIO
from PIL import Image

def resizeImg():
     #수정
    file = 'twopeople_test2.jpg'
    img = Image.open(file)
    img = img.resize((540, 780), Image.ANTIALIAS)
    img.save('twopeople_test2.jpg', quality=50)
def cal_tan(pos1, pos2):
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

resizeImg()

APP_KEY = 'cc945fdb4b2b7b18448576eeaaedca61'
IMAGE_URL ='twopeople_test2.jpg'
IMAGE_FILE_PATH = 'twopeople_test2.jpg'
session = requests.Session()
session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

# URL로 이미지 입력시
response = session.post('https://cv-api.kakaobrain.com/pose', data={'image_url': IMAGE_URL})
print(response.status_code, response.json())

#이미지 파일 불러오기
with open(IMAGE_FILE_PATH, 'rb') as f:
    response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', f)])
    print('응답코드',response.status_code, response.json())
    
    #keypoint 17개 좌표 데이터(x,y) 배열 생성
    #keypoints=response.json()[0]['keypoints']
    #point_array=[]
    #for i in range(0,len(keypoints)-2,3):
    #    point_array.append([keypoints[i],keypoints[i+1]])
    #print(point_array)
    
    keypoints1=response.json()[0]['keypoints']
    keypoints2=response.json()[1]['keypoints']
    
    keypoints1_arr=[]
    keypoints2_arr=[]
    
    for i in range(0,len(keypoints1)-2,3):
        keypoints1_arr.append([keypoints1[i],keypoints1[i+1]])
        keypoints2_arr.append([keypoints2[i],keypoints2[i+1]])
    
    print(keypoints1_arr)
    print(keypoints2_arr)

#기준값
pos_pivot = [[299.5312, 123.7031], [311.5848, 122.4844], [289.8884, 110.2969], [317.6116, 140.7656], [273.0134, 117.6094], [307.9688, 268.7344], [221.183, 196.8281], [369.442, 361.3594], [151.2723, 235.8281], [392.3438, 235.8281], [131.9866, 363.7969], [275.4241, 516.1406], [222.3884, 522.2344], [280.2455, 659.9531], [216.3616, 661.1719], [205.5134, 773.2969], [207.9241, 773.2969]]

#인물1 좌표데이터
pos_data1=keypoints1_arr
#인물2 좌표데이터
pos_data2=keypoints2_arr

#기준값 tan
tan_pivot=[]
#입력값 tan
tan_data1=[]
tan_data2=[]

for i in range (0, len(pos_pivot)-1):
    tan_pivot.append(cal_tan(pos_pivot[i], pos_pivot[i+1]))
    tan_data1.append(cal_tan(pos_data1[i], pos_data1[i+1]))
    tan_data2.append(cal_tan(pos_data2[i], pos_data2[i+1]))

#오차율 출력
print(abs(cal_error(tan_pivot, tan_data1, len(tan_pivot))))
print(abs(cal_error(tan_pivot, tan_data2, len(tan_pivot))))
    
