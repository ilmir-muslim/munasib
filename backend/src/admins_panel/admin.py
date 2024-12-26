from django.contrib import admin

from .models import Worker, Operations, Goods

admin.site.register(Worker)
admin.site.register(Operations)
admin.site.register(Goods)
