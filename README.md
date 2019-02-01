# photolens

Facilitates real time face detection feature using trained ML models

To run the django server locally, execute below command from project's folder in shell

```
pip install -r requirements.txt
```

```
python manage.py migrate
```

```
python manage.py runserver
```

To start using Please face towards your computer's webcam & execute following api in given sequence (on postman or browser):


## APIs

### Create Dataset
```
Endpoint: localhost:8000/lens/v1/create_dataset
```
Request Type: POST
Body: {userId: integer}

To create dataset for a user by capturing his facial patterns. Please specify his her userId as Integer type

### Train a Model
```
Endpoint: localhost:8000/lens/v1/trainer
```
Request Type: GET

To trigger training of new ML model

### Detect Face
```
Endpoint: localhost:8000/lens/v1/detect
```
Request Type: GET

To detect a person's face, & provide userId specified earlier for him


You can the APIs on any server by specifying the ip & port while starting the server. Also, please replace the localhost
& port(8000) in such case.
