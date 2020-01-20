from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from scraper import models
from unittest.mock import patch


class TasksApiTests(TestCase):
    fixtures = ["tasks.json"]

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_tasks_data(self):
        """
        Test retrieve Tasks.
        """
        task_count = models.Task.objects.all().count()
        response = self.client.get('/api/v1/scraper/tasks/', format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(task_count, len(response.data))

    def test_get_by_id_task_data(self):
        """
        Test get Task by id.
        """
        objects = models.Task.objects.all().first()
        response = self.client.get('/api/v1/scraper/tasks/{}/'.format(int(objects.id)), format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(objects.id, response.data['id'])

    @patch("scraper.tasks.start_new_task", return_value=True)
    def test_create_new_task_with_valid_url(self, start_task):
        """
        Test create Task with valid url address.
        """
        response = self.client.post('/api/v1/scraper/tasks/', {"url": "https://stackoverflow.com", "type": "image"},
                                    format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_create_new_task_with_invalid_url(self):
        """
        Test create Task with invalid url address.
        """
        response = self.client.post('/api/v1/scraper/tasks/', {"url": "stackoverflow.com", "type": "image"},
                                    format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ResurceApiTests(TestCase):
    fixtures = ["resourses.json", "tasks.json"]

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_resources_data(self):
        """
        Test retrieve Resources.
        """
        task_count = models.Resource.objects.all().count()
        response = self.client.get('/api/v1/scraper/resources/', format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(task_count, len(response.data))

    def test_get_by_id_resources_data(self):
        """
        Test get by id Task.
        """
        objects = models.Resource.objects.all().first()
        response = self.client.get('/api/v1/scraper/resources/{}/'.format(int(objects.id)), format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(objects.id, response.data['id'])
