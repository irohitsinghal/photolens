from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import cv2
import numpy as np
from PIL import Image

from django.utils.datastructures import MultiValueDictKeyError
from api.settings import BASE_DIR


samples_path = "/ml/dataset/"
recognizer_path = "/ml/recognizer/trainingData.yml"


@api_view(['POST'])
def create_dataset(request, version):
    print("OpenCv Version:", cv2.__version__)
    resStatus = status.HTTP_201_CREATED
    resMsg = "Successfully Created dataset for id: {}"

    try:
        # capture images from the webcam and process and detect the face
        cam = cv2.VideoCapture(0)
        id = request.POST['userId']
        resMsg.format(id)
        # Creating a cascade Image classifier
        faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        samples = 0
        # Capturing the faces one by one and detect the faces and showing it on the window
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for(x,y,w,h) in faces:
                samples = samples + 1
                # Saving the image dataset, only the face part
                cv2.imwrite(BASE_DIR + samples_path + 'user.'+str(id)+'.'+str(samples)+'.jpg', gray[y:y+h,x:x+w])
                cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
                cv2.waitKey(250)
            cv2.imshow("Face",img)
            cv2.waitKey(1)
            if(samples>5):
                break
    except MultiValueDictKeyError as e:
        resStatus = status.HTTP_400_BAD_REQUEST
        resMsg = "userId Parameter Missing."
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception Occurred in create dataset!"
    finally:
        if(cam != None):
            cam.release()
        cv2.destroyAllWindows()
    return Response(resMsg, status=resStatus)


@api_view(['GET'])
def trainer(request, version):
    print("API Version:", version)
    resStatus = status.HTTP_200_OK
    resMsg = 'Successfully Trained Model with dataset of {id} people samples'
    try:
        faces, ids = getImageswithId(BASE_DIR + samples_path)
        resMsg.format(id=len(set(ids)))
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, ids)
        recognizer.save(BASE_DIR+recognizer_path)
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception occurred"

    return Response(resMsg, status = resStatus)


def getImageswithId(path):
    import os
    imagePaths = [os.path.join(path, file) for file in os.listdir(path)]
    faces = []
    ids = []
    for imagepath in imagePaths:
        faceimg = Image.open(imagepath).convert('L') #convert it to grayscale
        facenp = np.array(faceimg, 'uint8')
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(facenp)
        ids.append(ID)
        cv2.imshow("training", facenp)
        cv2.waitKey(50)
    cv2.destroyAllWindows()
    return np.array(faces), np.array(ids)


@api_view(['GET'])
def detect(request, version):
    print("API Version:", version)
    resStatus = status.HTTP_200_OK
    resMsg = "Person id: "
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(BASE_DIR + recognizer_path)
        cam = cv2.VideoCapture(0)
        ret, img = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        id = recognizer.predict(gray)
        resMsg += str(id)
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception occurred"

    return Response(resMsg, status = resStatus)
