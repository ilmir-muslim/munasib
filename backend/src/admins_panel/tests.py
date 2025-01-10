from django.test import TestCase
from admins_panel.models import Worker, Operations, WorksDone


class WorkerSalaryTests(TestCase):
    def setUp(self):
        self.worker = Worker.objects.create(name="Test Worker", salary=0)
        self.operation = Operations.objects.create(name="Test Operation", price=100)

    def test_salary_update_on_work_done(self):
        WorksDone.objects.create(
            worker=self.worker, operation=self.operation, quantity=5
        )
        self.worker.refresh_from_db()  # Обновляем данные из базы
        self.assertEqual(self.worker.salary, 500)
