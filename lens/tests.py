from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

import json
from random import randint


# Create your tests here.


class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        self.id = randint(10, 100)
        self.scsMsg = "Successfully Created dataset for id: {}".format(self.id)
        self.missMsg = "userId Parameter Missing."
        self.errorMsg = "Exception Occurred in create dataset!"


class DataSetCreationTestCases(BaseViewTest):

    def successfulDatasetCreationCase(self):
        response = self.client.post(
            reverse("create_dataset", kwargs={"version": "v1"}),
            data=json.dump({'userId': self.id}),
            content_type='application/json'
        )
        self.assertEqual(response.data, self.scsMsg)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def ParameterMissingCase(self):
        response = self.client.post(
            reverse("create_dataset", kwargs={"version": "v1"}),
            data=json.dump({}),
            content_type='application/json'
        )
        self.assertEqual(response.data, self.missMsg)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
