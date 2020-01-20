from rest_framework.test import APIClient
from unittest import TestCase
from django.urls import reverse
from rest_framework import status


class DownloadViewModel1Api(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_not_found(self):
        response = self.client.get(reverse('download') + '/{}/'.format(int(123)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
