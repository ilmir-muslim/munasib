from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OperationLog, GoodsLog

@receiver(post_save, sender=OperationLog)
def add_goods_log_on_operation_log(sender, instance, created, **kwargs):
    """
    Сигнал для добавления записи в GoodsLog при добавлении записи в OperationLog.
    """
    if created and instance.operation.add_goods:  # Проверяем, нужно ли добавлять товар
        # Создаём запись в GoodsLog
        GoodsLog.objects.create(
            worker=instance.worker,          # Указываем работника
            goods=instance.goods,              # Товар из операции
            quantity=instance.quantity,      # Количество из OperationLog
            release_date=instance.date,      # Дата из OperationLog
        )
