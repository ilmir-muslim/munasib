from rest_framework import serializers


class OperationRecordSerializer(serializers.Serializer):
    worker_id = serializers.IntegerField()
    operation_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
