from decimal import Decimal

from django.http import JsonResponse
from admins_panel.models import Worker, Operation


def process_operation(worker_id, operation_id, quantity):
    worker = Worker.objects.get(id=worker_id)
    operation = Operation.objects.get(id=operation_id)
    amount = operation.price * quantity
    worker.add_salary(amount)


def pay_salary(worker_id, amount):
    worker = Worker.objects.get(id=worker_id)
    worker.deduct_salary(Decimal(amount))


def check_id_telegram(request, id_telegram):
    try:
        Worker.objects.get(id_telegram=id_telegram)
        return JsonResponse({"exists": True})
    except Worker.DoesNotExist:
        return JsonResponse({"exists": False})

def register_new_user(request, name, work_place, id_telegram):
    Worker.objects.create(name=name, work_place=work_place, id_telegram=id_telegram)
    return JsonResponse({"message": "User successfully registered."})