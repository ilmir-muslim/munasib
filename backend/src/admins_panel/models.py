from django.db import models
from django.utils.translation import gettext_lazy as _


class Worker(models.Model):
    name = models.CharField(_("Работник"), max_length=50)
    work_place = models.CharField(_("Место работы"), max_length=50)
    admins_rights = models.BooleanField(_("Права админа"), default=False)
    salary = models.DecimalField(_("зарплата"), max_digits=10, decimal_places=2, default=0)
    class Meta:
        verbose_name = _("Работник")
        verbose_name_plural = _("Работники")

    def __str__(self):
        return self.name
    
    def add_salary(self, amount):
        self.salary += amount
        self.save()

    def deduct_salary(self, amount):
        self.salary -= amount
        self.save()


class Operations(models.Model):
    name = models.CharField(_("Операции"), max_length=50)
    price = models.DecimalField(_("Цена операции"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Операция")
        verbose_name_plural = _("Операции")

    def __str__(self):
        return self.name

class WorksDone(models.Model):
    name = models.CharField(_("Выполненные работы"), max_length=50)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Дата выполнения работ"))
    quantity = models.IntegerField(_("Количество выполненных работ"))

    class Meta:
        verbose_name = _("Выполненная работа")
        verbose_name_plural = _("Выполненные работы")

    def __str__(self):
        return self.name

class Goods(models.Model):
    name = models.CharField(_("Товар"), max_length=50)
    price = models.DecimalField(_("Цена товара"), max_digits=10, decimal_places=2)
    quantity = models.IntegerField(_("Количество товара"))

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.name
