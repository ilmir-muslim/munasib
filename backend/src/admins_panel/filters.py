from django import forms
import django_filters
from .models import Operation, OperationLog, Worker


class OperationLogFilter(django_filters.FilterSet):
    operation = django_filters.ModelChoiceFilter(
        queryset=Operation.objects.all(),
        label="العملية",  # Операция -> العملية
        widget=forms.Select(attrs={'class': 'select2'})
    )
    worker = django_filters.ModelChoiceFilter(
        queryset=Worker.objects.all(),
        label="الموظف",  # Работник -> الموظف
        widget=forms.Select(attrs={'class': 'select2'})
    )

    class Meta:
        model = OperationLog
        fields = ["operation", "worker"]