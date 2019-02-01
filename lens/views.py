from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# import pdb; pdb.set_trace()

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
    resMsg = "Successfully Created dataset for id: "

    try:
        # capture images from the webcam and process and detect the face
        cam = cv2.VideoCapture(0)
        id = request.POST['userId']
        resMsg += str(id)
        # Creating a cascade Image classifier
        faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        samples = 0
        # Capturing the faces one by one and detect the faces and showing it on the window
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                samples = samples + 1
                # Saving the image dataset, only the face part
                cv2.imwrite(BASE_DIR + samples_path + 'user.' + str(id) + '.' + str(samples) + '.jpg',
                            gray[y:y + h, x:x + w])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.waitKey(250)
            cv2.imshow("Face", img)
            cv2.waitKey(1)
            if (samples > 10):
                break
    except MultiValueDictKeyError as e:
        resStatus = status.HTTP_400_BAD_REQUEST
        resMsg = "userId Parameter Missing."
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception Occurred in create dataset!"
    finally:
        if (cam != None):
            cam.release()
        cv2.destroyAllWindows()
    return Response(resMsg, status=resStatus)


@api_view(['GET'])
def trainer(request, version):
    print("API Version:", version)
    resStatus = status.HTTP_200_OK
    resMsg = 'Successfully Trained Model with dataset of'
    try:
        faces, ids = getImageswithId(BASE_DIR + samples_path)
        if (len(faces) == 0):
            raise FileNotFoundError
        resMsg = resMsg + str(len(set(ids))) + "people samples"
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(faces, ids)
        recognizer.save(BASE_DIR + recognizer_path)
    except FileNotFoundError as e:
        resStatus = status.HTTP_400_BAD_REQUEST
        resMsg = "No dataset found to train model, please run create_dataset api first"
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception occurred"

    return Response(resMsg, status=resStatus)


def getImageswithId(path):
    import os
    imagePaths = [os.path.join(path, file) for file in os.listdir(path)]
    faces = []
    ids = []
    for imagepath in imagePaths:
        faceimg = Image.open(imagepath).convert('L')  # convert it to grayscale
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

    userid = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    try:
        cam = cv2.VideoCapture(0)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(BASE_DIR + recognizer_path)
        faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                getId, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if (conf > 35):
                    userid = getId
                    cv2.putText(img, "Detected", (x + w, y + h), font, 2, (0, 255, 0), 2)
                else:
                    cv2.putText(img, "Unknown", (x, y + h), font, 2, (0, 0, 255), 2)
                cv2.waitKey(250)
            cv2.imshow("Face", img)
            if (cv2.waitKey(1) == ord('q') or userid != 0):
                cv2.waitKey(1000)
                break
    except cv2.error as e:
        resStatus = status.HTTP_400_BAD_REQUEST
        resMsg = "No trained model found to predict, please run trainer api first"
    except:
        resStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
        resMsg = "Exception occurred"
    finally:
        cam.release()
        cv2.destroyAllWindows()
    resMsg += str(userid)
    return Response(resMsg, status=resStatus)
