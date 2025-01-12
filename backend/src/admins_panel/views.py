from django_tables2 import SingleTableView

from admins_panel.tables import WorkerTable
from .models import Worker

class WorkerListView(SingleTableView):
    model = Worker
    table_class = WorkerTable
    template_name = "admins_panel/workers_list.html"
