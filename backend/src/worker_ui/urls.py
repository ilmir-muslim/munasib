from django.urls import path
from .views import pay_salary_view, process_operation_view

urlpatterns = [
    path("workers/<int:worker_id>/pay_salary/", pay_salary_view, name="pay_salary_view"),
    path(
        "workers/<int:worker_id>/operations/<int:operation_id>/process/",
        process_operation_view,
        name="process_operation_view",
    ),
]
