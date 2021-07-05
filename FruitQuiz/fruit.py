## Import
# (1)
import random
#import sound

# (2)

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

# (3)
# 라즈베리 캠 추가
import cv2


## Settings
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')

ansDict = {0: '사과', 1: '바나나', 2: '포도', 3: '딸기', 4: '레몬', 5: 0} # 해당 퀴즈에서 과일의 종류는 다음과 같습니다.



## 문제 출제 (1번 게임 코드 활용)
def random_List(imageNum, maxImageNum):
    result = []

    for v in range(maxImageNum):
        result.append(v)
        random.shuffle(result)

    return result[0:imageNum]


def makeQuiz():
    #global answerList

    answerIndex = randList[-1]

    ans = ansDict[answerIndex]

    if not ans == 0:
        ## 출력 부분 추가 (출력문 or UI) - 현경
        print(str(ans) + ' 를 들고오세요.')
        print(str(ans) + ' 를 보여주세요.')
        quizStart(ans)
    else:
        return 1

def quizStart(ans):
    # 카메라 열기
    cap = cv2.VideoCapture(0)

    while (True):
        # 카메라로 부터 사진 한장 읽기
        ret, frame = cap.read()

        # 얼굴 검출 시도

        cv2.imwrite('test.jpg', frame)
        #cv2.imshow('frame_color', frame)
        prediction = pred('test.jpg') # 모델에 추론 이미지 인풋

        # 정답 확인.
        if ansDict[0] == ans and prediction[0][0] >= 0.6:
            # 정답
            #sound.correctSound()
            print('사과 Correct !!')
            break

        elif ansDict[1] == ans and prediction[0][1] >= 0.6:
            # 정답
            #sound.correctSound()
            print('바나나 Correct !!')
            break

        elif ansDict[2] == ans and prediction[0][2] >= 0.6:
            # 정답
            #sound.correctSound()
            print('포도 Correct !!')
            break

        elif ansDict[3] == ans and prediction[0][3] >= 0.6:
            # 정답
            #sound.correctSound()
            print('딸기 Correct !!')
            break

        elif ansDict[4] == ans and prediction[0][4] >= 0.6:
            # 정답
            #sound.correctSound()
            print('레몬 Correct !!')
            break
        else:
            continue


## (2) 티처블 머신 학습된 모델 코드
def pred(inference_data_path): #.jpg 타입
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(inference_data_path)

    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)

    # display the resized image
    #image.show()

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    #print(prediction) ## 출력 결과 (각 Class별 확률값)pre

    ###prediction = [0, 0, 0.7, 0.3, 0]
    ###print(ans[0])

    return prediction





## 과일 퀴즈 시작 (main)
questionNum = 10	#출제 문제 갯수

count = questionNum

while count > 0:
    randList = random_List(questionNum, len(ansDict))
    makeQuiz() ## makeQuiz() -> 내 quizStart() 작동 -> 그 안에서 정답판별 및 처리하는 구조,,
    count -= 1



#print("정답 갯수: " + str(countTrue))
#print("오답 갯수: " + str(countFalse))
#print("정답률: " + str(countTrue/questionNum*100) +  '%')
#print("점수:  " +str(score) + '점')
