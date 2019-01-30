from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import cv2

from django.utils.datastructures import MultiValueDictKeyError
from api.settings import BASE_DIR


def index():
    return Response("Try me!")


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
                cv2.imwrite(BASE_DIR+'/ml/dataset/user.'+str(id)+'.'+str(samples)+'.jpg', gray[y:y+h,x:x+w])
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
