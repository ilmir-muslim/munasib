from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import pay_salary, process_operation


@api_view(["POST"])
def pay_salary_view(request, worker_id):
    amount = request.data.get("amount")
    pay_salary(worker_id, amount)
    return Response({"status": "salary deducted"}, status=200)


@api_view(["POST"])
def process_operation_view(request, worker_id, operation_id):
    quantity = int(request.data.get("quantity"))
    process_operation(worker_id, operation_id, quantity)
    return Response({"status": "operation processed"}, status=200)
