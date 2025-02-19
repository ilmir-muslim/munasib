import django_tables2 as tables
from .models import Worker, OperationLog

class WorkerTable(tables.Table):
    name = tables.Column(verbose_name="الاسم")
    work_place = tables.Column(verbose_name="مكان العمل")
    admins_rights = tables.Column(verbose_name="حقوق الإدارة")
    salary = tables.Column(verbose_name="الراتب")

    class Meta:
        model = Worker
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "work_place", "admins_rights", "salary")

class OperationLogTable(tables.Table):
    worker = tables.Column(verbose_name="العامل")
    operation = tables.Column(verbose_name="العملية")
    date = tables.Column(verbose_name="التاريخ")
    quantity = tables.Column(verbose_name="الكمية")

    class Meta:
        model = OperationLog
        template_name = "django_tables2/bootstrap4.html"
        fields = ("worker", "operation", "date", "quantity")