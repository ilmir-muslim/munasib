from rest_framework import serializers

from admins_panel.models import Operation


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'  # Или укажите конкретные поля: ['id', 'name', ...]
