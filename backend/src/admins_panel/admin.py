from django.contrib import admin

from .models import Worker, Operations, Goods, WorksDone


class WorkerAdmin(admin.ModelAdmin):
    fields = ["name", "work_place", "admins_rights"]
    readonly_fields = ["salary"]

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Operations)
admin.site.register(Goods)
admin.site.register(WorksDone)
