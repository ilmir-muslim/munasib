from datetime import datetime, timedelta
from django.db.models import Sum
from django.views.generic import TemplateView
from django_tables2 import SingleTableView
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from .filters import OperationLogFilter
from .tables import OperationLogTable, WorkerTable
from .models import OperationLog, Worker


class HomePageView(TemplateView):
    template_name = "base.html"


class WorkerListView(SingleTableView):
    model = Worker
    table_class = WorkerTable
    template_name = "admins_panel/workers_list.html"


class OperationLogListView(SingleTableMixin, FilterView):
    model = OperationLog
    table_class = OperationLogTable
    template_name = "admins_panel/operation_log.html"
    filterset_class = OperationLogFilter

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if start_date:
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                queryset = queryset.filter(date__gte=start_date)
            except ValueError:
                pass

        if end_date:
            try:
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date() + timedelta(
                    days=1
                )
                queryset = queryset.filter(date__lt=end_date)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используем отфильтрованный набор данных
        filtered_queryset = self.filterset.qs
        # Подсчитываем сумму по всем отфильтрованным строкам
        total_value = filtered_queryset.aggregate(total=Sum("quantity"))["total"] or 0
        print("Total value:", total_value)

        if total_value is None:
            total_value = 0

        context["total_value"] = total_value
        return context
