from django.urls import path

from admins_panel.views import WorkerListView


urlpatterns = [
    path("workers_list/", WorkerListView.as_view(), name="workers_list"),
    ]
