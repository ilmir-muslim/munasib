from django.contrib import admin

from .models import Worker, Operation, Goods, OperationLog, Position


admin.site.register(Worker)
admin.site.register(Operation)
admin.site.register(Goods)
admin.site.register(OperationLog)
admin.site.register(Position)
