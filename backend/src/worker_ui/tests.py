from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from admins_panel.models import Worker, Operations

class WorkerUITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.worker = Worker.objects.create(id=1, name="Test Worker", salary=0)
        self.operation = Operations.objects.create(id=1, name="Test Operation", price=100)

    def test_pay_salary(self):
        url = reverse('pay_salary_view', kwargs={'worker_id': self.worker.id})
        print(f"Testing URL: {url}")  # Добавьте эту строку для отладки
        response = self.client.post(url, data={'amount': 1000})
        print(f"Response status code: {response.status_code}")  # Добавьте эту строку для отладки
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_process_operation(self):
        url = reverse('process_operation_view', kwargs={'worker_id': self.worker.id, 'operation_id': self.operation.id})
        print(f"Testing URL: {url}")  # Добавьте эту строку для отладки
        response = self.client.post(url, data={'quantity': 10})
        print(f"Response status code: {response.status_code}")  # Добавьте эту строку для отладки
        self.assertEqual(response.status_code, status.HTTP_200_OK)
