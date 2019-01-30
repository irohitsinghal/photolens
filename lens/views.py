from django.shortcuts import render, redirect
import cv2

from api.settings import BASE_DIR

# Create your views here.


def create_dataset(request, version):
    id = request.POST['userId']
    print(cv2.__version__)
    # Detect Face
    # Creating a cascade Image classifier
    faceDetect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # camture images from the webcam and process and detect the face
    cam = cv2.VideoCapture(0)

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

    cam.release()
    cv2.destroyAllWindows()

    return redirect('/')
