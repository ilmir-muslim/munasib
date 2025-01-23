from django.urls import path

from admins_panel.views import OperationLogListView, WorkerListView


urlpatterns = [
    path("workers_list/", WorkerListView.as_view(), name="workers_list"),
    path("operation_log/", OperationLogListView.as_view(), name="operation_log_list"),
    ]
