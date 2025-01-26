from django.contrib import admin

from .models import GoodsLog, Worker, Operation, Goods, OperationLog, Position


admin.site.register(Worker)
admin.site.register(Operation)
admin.site.register(Goods)
admin.site.register(OperationLog)
admin.site.register(GoodsLog)
admin.site.register(Position)
