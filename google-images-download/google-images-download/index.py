from google_images_download import google_images_download as ggid
import os
from os import remove

from google.cloud import vision
from PIL import Image, ImageDraw

#Google Vision API Key json파일 지정
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\jungu\\Downloads\\crucial-botany-318311-a877288b959d.json"

#얼굴 탐지 함수
def detect_face(face_file, max_results=1): #max_results : 최대 얼굴객체 검출수
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = vision.Image(content=content)
    return client.face_detection(
        image=image, max_results=max_results).face_annotations

"""
#검출한 얼굴 객체에 네모박스 그리기 + 결과 이미지 저장(해당 함수는 현 프로젝트에서 실행하지 않아도 됨)
def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000')
    im.save(output_filename)
"""

def main():
    #크롤링 후 이미지파일이 저장될 디렉터리 경로
    file_path='C:\\Users\\jungu\\OneDrive\\Desktop\\팀 프로젝트\\google-images-download\\google-images-download\\downloads\\'+category
    #디렉터리 내의 인물 이름 리스트에 저장
    file_names=os.listdir(file_path)

    for file in enumerate(file_names):
        #읽어올 이미지(파일경로 + 파일이름)
        f=file_path+'\\'+str(file[1])
        with open(f, 'rb') as image:
            faces = detect_face(image, 4)
            if len(faces)==1:
                print('{} ==> Found {} face'.format(str(file[1]),len(faces)))
            else:
                image.close()
                os.remove(f)
                print('{} ==> Delete : Found more than 2 faces'.format(str(file[1])))

if __name__ == '__main__':
    #크롤링 대상 키워드
    category = input("검색어 입력: ")
    #Google Image Download 사용을 위한 함수
    response = ggid.googleimagesdownload()
    # limit - 사진수
    arguments = {"keywords":category,"limit":20,"print_urls":True,"format":"jpg"}
    
    paths = response.download(arguments)
    print(paths)
    main()