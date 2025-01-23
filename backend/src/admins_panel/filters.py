import django_filters
from .models import OperationLog


class OperationLogFilter(django_filters.FilterSet):
    operation = django_filters.CharFilter(
        field_name="operation__name", lookup_expr="icontains", label="Операция"
    )
    worker = django_filters.CharFilter(
        field_name="worker__name", lookup_expr="icontains", label="Работник"
    )

    class Meta:
        model = OperationLog
        fields = ["operation", "worker"]