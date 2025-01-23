import django_tables2 as tables
from .models import Worker, OperationLog

class WorkerTable(tables.Table):
    class Meta:
        model = Worker
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "work_place", "admins_rights", "salary")

class OperationLogTable(tables.Table):
    class Meta:
        model = OperationLog
        template_name = "django_tables2/bootstrap4.html"
        fields = ("worker", "operation", "date", "quantity")