from django.contrib import admin

from .models import Worker, Operation, Goods, OperationLog


admin.site.register(Worker)
admin.site.register(Operation)
admin.site.register(Goods)
admin.site.register(OperationLog)
