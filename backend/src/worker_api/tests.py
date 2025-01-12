from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from admins_panel.models import Operation, OperationLog, Worker
from worker_api.services import check_id_telegram


# class RecordOperationViewTests(APITestCase):
#     def setUp(self):
#         self.worker = Worker.objects.create(name="Test Worker")
#         self.operation = Operation.objects.create(name="Test Operation")
#         self.url = reverse("record-operation")

#     def test_record_operation_success(self):
#         data = {
#             "worker_id": self.worker.id,
#             "operation_id": self.operation.id,
#             "quantity": 10,
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data["message"], "Operation recorded successfully")
#         self.assertTrue(
#             OperationLog.objects.filter(
#                 worker=self.worker, operation=self.operation, quantity=10
#             ).exists()
#         )

#     def test_record_operation_worker_not_found(self):
#         data = {"worker_id": 999, "operation_id": self.operation.id, "quantity": 10}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Worker not found")

#     def test_record_operation_operation_not_found(self):
#         data = {"worker_id": self.worker.id, "operation_id": 999, "quantity": 10}
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["error"], "Operation not found")

#     def test_record_operation_invalid_data(self):
#         data = {
#             "worker_id": self.worker.id,
#             "operation_id": self.operation.id,
#             "quantity": "invalid",
#         }
#         response = self.client.post(self.url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CheckTelegramIdTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.worker = Worker.objects.create(name="Test Worker", id_telegram=12345)

    def test_valid_id_telegram(self):
        request = self.factory.get("/fake-url/")
        response = check_id_telegram(request, 12345)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"exists": True})

    def test_invalid_id_telegram(self):
        request = self.factory.get("/fake-url/")
        response = check_id_telegram(request, 67890)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"exists": False})

    def test_empty_id_telegram(self):
        request = self.factory.get("/fake-url/")
        response = check_id_telegram(request, None)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"exists": False})
