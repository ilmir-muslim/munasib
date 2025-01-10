from decimal import Decimal
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Worker(models.Model):
    name = models.CharField("Работник", max_length=50)
    work_place = models.CharField("Место работы", max_length=50)
    admins_rights = models.BooleanField("Права админа", default=False)
    salary = models.DecimalField("зарплата", max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return self.name

    def add_salary(self, amount):
        self.salary += Decimal(amount)
        self.save()

    def deduct_salary(self, amount):
        self.salary -= Decimal(amount)
        self.save()


class Operations(models.Model):
    name = models.CharField("Операции", max_length=50)
    price = models.DecimalField("Цена операции", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self):
        return self.name

class WorksDone(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата выполнения работ", default=now)
    quantity = models.IntegerField("Количество выполненных работ")

    class Meta:
        verbose_name = "Выполненная работа"
        verbose_name_plural = "Выполненные работы"

    def __str__(self):
        return f'Операция: {self.operation.name}, выполнил: {self.worker.name}'

@receiver(post_save, sender=WorksDone)
def update_worker_salary(sender, instance, created, **kwargs):
    if created:
        amount = instance.operation.price * instance.quantity
        instance.worker.add_salary(amount)

class Goods(models.Model):
    name = models.CharField("Товар", max_length=50)
    price = models.DecimalField("Цена товара", max_digits=10, decimal_places=2)
    quantity = models.IntegerField("Количество товара")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name
