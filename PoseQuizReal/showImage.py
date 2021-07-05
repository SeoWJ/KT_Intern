import numpy as np
from matplotlib import image as mpimg
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
from requests import Session
import cv2


#수정
from io import StringIO
from PIL import Image

APP_KEY = 'cc945fdb4b2b7b18448576eeaaedca61'
session = Session()

session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})


def inference(filename):
    with open(filename, 'rb') as f:
        response = session.post('https://cv-api.kakaobrain.com/pose', files={'file': f})
        response.raise_for_status()
        return response.json()


def visualize(filename, annotations, threshold=0.2):
    # 낮은 신뢰도를 가진 keypoint들은 무시
    for annotation in annotations:
        keypoints = np.asarray(annotation['keypoints']).reshape(-1, 3)
        low_confidence = keypoints[:, -1] < threshold
        keypoints[low_confidence, :] = [0, 0, 0]
        annotation['keypoints'] = keypoints.reshape(-1).tolist()

    # COCO API를 활용한 시각화
    plt.imshow(mpimg.imread(filename))
    plt.axis('off')
    coco = COCO()
    coco.dataset = {
        "categories": [
            {
                "supercategory": "person",
                "id": 1,
                "name": "person",
                "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder",
                              "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip",
                              "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"],
                "skeleton": [[1, 2], [1, 3], [2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 7], [6, 8], [6, 12], [7, 9],
                             [7, 13], [8, 10], [9, 11], [12, 13], [14, 12], [15, 13], [16, 14], [17, 15]]
            }
        ]
    }
    coco.createIndex()
    coco.showAnns(annotations)
    #에러가 나서 이미지로 저장하고 다시 그 이미지를 띄움
    #plt.show()
    
    # modify
    
   
    plt.savefig('/home/pi/real_test.jpg')
    img = cv2.imread('/home/real_test.jpg', cv2.IMREAD_UNCHANGED)
    
    
    cv2.imshow('Result', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def resizeImg():
     #수정
    file = '/home/pi/real_test.jpg'
    #file2 = 'white.jpg'
    img = Image.open(file)
    img = img.resize((540, 780), Image.ANTIALIAS)
    img.save('/home/pi/real_test.jpg', quality=50)
    
    #img = Image.open(file)
    #img = img.resize((540, 780), Image.ANTIALIAS)
    #img.save('white.jpg', quality=50)

    
    
resizeImg()
IMAGE_FILE_PATH = '/home/pi/real_test.jpg'
result = inference(IMAGE_FILE_PATH)
visualize(IMAGE_FILE_PATH, result)
#visualize('white.jpg', result)
