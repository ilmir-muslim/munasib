from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Operation(models.Model):
    name = models.CharField("Операции", max_length=50)
    price = models.FloatField("Цена операции")
    add_goods = models.BooleanField("Добавление товара", default=False)


    class Meta:
        verbose_name = "Операция"
        verbose_name_plural = "Операции"

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField("Должность", max_length=50)
    default_operation = models.ForeignKey(
        Operation, on_delete=models.SET_NULL, null=True, blank=True
    )
    admins_rights = models.BooleanField("Права админа", default=False)


    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField("Работник", max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    telegram_id = models.IntegerField("ID телеграм", unique=True, null=True)
    have_telegram = models.BooleanField("Есть телеграм", default=True)
    salary = models.FloatField("зарплата", default=0)

    @staticmethod
    def get_deleted_worker():
        return Worker.objects.get_or_create(
            name="Удаленный работник", defaults={"salary": 0}
        )[0]

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"

    def __str__(self):
        return self.name

    def add_salary(self, amount):
        self.salary += amount
        self.save()

    def deduct_salary(self, amount):
        self.salary -= amount
        self.save()


class OperationLog(models.Model):
    worker = models.ForeignKey(
        Worker, on_delete=models.SET_DEFAULT, default=Worker.get_deleted_worker
    )
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата выполнения работ", default=now)
    quantity = models.IntegerField("Количество выполненных работ")
    goods = models.ForeignKey(  # Ссылка на существующий товар
        "Goods",
        on_delete=models.CASCADE,
        verbose_name="Товар",
        null=True,
        blank=True,  # Если операция не связана с товаром
    )

    class Meta:
        verbose_name = "Выполненная работа"
        verbose_name_plural = "Выполненные работы"

    def __str__(self):
        return f"Операция: {self.operation.name}, выполнил: {self.worker.name}"


@receiver(post_save, sender=OperationLog)
def update_worker_salary(sender, instance, created, **kwargs):
    if created:
        amount = instance.operation.price * instance.quantity
        instance.worker.add_salary(amount)


class Goods(models.Model):
    name = models.CharField("Товар", max_length=50)
    price = models.FloatField("Цена товара")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class GoodsLog(models.Model):
    worker = models.ForeignKey(
        Worker, on_delete=models.SET_DEFAULT, default=Worker.get_deleted_worker
    )
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.IntegerField("Количество товара")
    release_date = models.DateField("Дата выпуска товара", default=now)
    selling_date = models.DateField("Дата продажи товара", null=True, blank=True)

    class Meta:
        verbose_name = "Выпущенный товар"
        verbose_name_plural = "Выпущенные товары"

    def __str__(self):
        return f"Товар: {self.goods.name}, выпустил: {self.worker.name}"
