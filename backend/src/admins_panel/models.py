from django.db import models
from django.utils.translation import gettext_lazy as _


class Worker(models.Model):
    name = models.CharField(_("Работника"), max_length=50)
    work_place = models.CharField(_("Место работы"), max_length=50)
    admins_rights = models.BooleanField(_("Права админа"), default=False)

    class Meta:
        verbose_name = _("Работник")
        verbose_name_plural = _("Работники")

    def __str__(self):
        return self.name


class Operations(models.Model):
    name = models.CharField(_("Операции"), max_length=50)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    date = models.DateTimeField(_("Дата выполнения операции"))
    time = models.DurationField(_("Время выполнения операции"))
    quantity = models.IntegerField(_("Количество выполненных операций"))
    price = models.DecimalField(_("Цена операции"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Операция")
        verbose_name_plural = _("Операции")

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
