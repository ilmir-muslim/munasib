from rest_framework import serializers
from admins_panel.models import Position, Operation

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'name', 'price']  # Добавьте другие поля, если нужно

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'default_operation']
