from calendar import c
from pyexpat import model
import django_tables2 as tables
from .models import Worker

class WorkerTable(tables.Table):
    class Meta:
        model = Worker
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "work_place", "admins_rights", "salary")
