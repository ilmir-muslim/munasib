from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Operation(models.Model):
    name = models.CharField("العملية", max_length=50)  # Операции -> العملية
    price = models.FloatField("سعر العملية")  # Цена операции -> سعر العملية
    add_goods = models.BooleanField("إضافة سلعة", default=False)  # Добавление товара -> إضافة سلعة

    class Meta:
        verbose_name = "العملية"  # Операция -> العملية
        verbose_name_plural = "العمليات"  # Операции -> العمليات

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField("المنصب", max_length=50)  # Должность -> المنصب
    default_operation = models.ForeignKey(
        Operation, on_delete=models.SET_NULL, null=True, blank=True
    )
    admins_rights = models.BooleanField("صلاحيات المدير", default=False)  # Права админа -> صلاحيات المدير

    class Meta:
        verbose_name = "المنصب"  # Должность -> المنصب
        verbose_name_plural = "المناصب"  # Должности -> المناصب

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField("الموظف", max_length=50)  # Работник -> الموظف
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)
    telegram_id = models.IntegerField("معرف التليجرام", unique=True, null=True)  # ID телеграм -> معرف التليجرام
    have_telegram = models.BooleanField("لديه تليجرام", default=True)  # Есть телеграм -> لديه تليجرام
    salary = models.FloatField("الراتب", default=0)  # зарплата -> الراتب

    @staticmethod
    def get_deleted_worker():
        return Worker.objects.get_or_create(
            name="موظف محذوف", defaults={"salary": 0}  # Удаленный работник -> موظف محذوف
        )[0]

    class Meta:
        verbose_name = "الموظف"  # Работник -> الموظف
        verbose_name_plural = "الموظفون"  # Работники -> الموظفون

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
    date = models.DateTimeField("تاريخ تنفيذ العمل", default=now)  # Дата выполнения работ -> تاريخ تنفيذ العمل
    quantity = models.IntegerField("كمية الأعمال المنفذة")  # Количество выполненных работ -> كمية الأعمال المنفذة
    goods = models.ForeignKey(  # Ссылка на существующий товар
        "Goods",
        on_delete=models.CASCADE,
        verbose_name="السلعة",  # Товар -> السلعة
        null=True,
        blank=True,  # Если операция не связана с товаром
    )

    class Meta:
        verbose_name = "العمل المنفذ"  # Выполненная работа -> العمل المنفذ
        verbose_name_plural = "الأعمال المنفذة"  # Выполненные работы -> الأعمال المنفذة

    def __str__(self):
        return f"العملية: {self.operation.name}, المنفذ: {self.worker.name}, التاريخ: {self.date}"  # Операция -> العملية, выполнил -> المنفذ, дата -> التاريخ


@receiver(post_save, sender=OperationLog)
def update_worker_salary(sender, instance, created, **kwargs):
    if created:
        amount = instance.operation.price * instance.quantity
        instance.worker.add_salary(amount)


class Goods(models.Model):
    name = models.CharField("السلعة", max_length=50)  # Товар -> السلعة
    price = models.FloatField("سعر السلعة")  # Цена товара -> سعر السلعة

    class Meta:
        verbose_name = "السلعة"  # Товар -> السلعة
        verbose_name_plural = "السلع"  # Товары -> السلع

    def __str__(self):
        return self.name


class GoodsLog(models.Model):
    worker = models.ForeignKey(
        Worker, on_delete=models.SET_DEFAULT, default=Worker.get_deleted_worker
    )
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.IntegerField("كمية السلعة")  # Количество товара -> كمية السلعة
    release_date = models.DateField("تاريخ إصدار السلعة", default=now)  # Дата выпуска товара -> تاريخ إصدار السلعة
    selling_date = models.DateField("تاريخ بيع السلعة", null=True, blank=True)  # Дата продажи товара -> تاريخ بيع السلعة

    class Meta:
        verbose_name = "السلعة المصدرة"  # Выпущенный товар -> السلعة المصدرة
        verbose_name_plural = "السلع المصدرة"  # Выпущенные товары -> السلع المصدرة

    def __str__(self):
        return f"السلعة: {self.goods.name}, المصدر: {self.worker.name}, تاريخ الإصدار: {self.release_date}"  # Товар -> السلعة, выпустил -> المصدر, дата выпуска -> تاريخ الإصدار