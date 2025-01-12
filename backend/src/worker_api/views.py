from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admins_panel.models import Operation, OperationLog, Worker


class RecordOperationView(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def post(self, request, *args, **kwargs):
        # Извлечение данных из запроса
        worker_id = request.data.get("worker_id")
        operation_id = request.data.get("operation_id")
        quantity = request.data.get("quantity")

        # Валидация входных данных
        if not all([worker_id, operation_id, quantity]):
            return Response(
                {"error": "worker_id, operation_id, and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            return Response(
                {"error": "quantity must be a positive integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверка существования работника и операции
        try:
            worker = Worker.objects.get(id=worker_id)
        except Worker.DoesNotExist as exc:
            raise NotFound({"error": f"Worker with id {worker_id} not found."}) from exc

        try:
            operation = Operation.objects.get(id=operation_id)
        except Operation.DoesNotExist as exc:
            raise NotFound({"error": f"Operation with id {operation_id} not found."}) from exc

        # Создание записи OperationLog
        OperationLog.objects.create(
            worker=worker, operation=operation, quantity=quantity
        )

        # Ответ пользователю
        return Response(
            {"message": "Operation successfully recorded."},
            status=status.HTTP_201_CREATED,
        )

class CheckTelegramIdView(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def get(self, request, id_telegram):
        try:
            Worker.objects.get(id_telegram=id_telegram)
            return Response({"exists": True})
        except Worker.DoesNotExist:
            return Response({"exists": False})
        
        
class RegisterNewUserView(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def post(self, request):
        # Извлечение данных из запроса
        name = request.data.get("name")
        work_place = request.data.get("work_place")
        id_telegram = request.data.get("id_telegram")

        # Валидация входных данных
        if not all([name, work_place, id_telegram]):
            return Response(
                {"error": "name, work_place, and id_telegram are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создание нового пользователя
        Worker.objects.create(name=name, work_place=work_place, id_telegram=id_telegram)

        # Ответ пользователю
        return Response(
            {"message": "User successfully registered."},
            status=status.HTTP_201_CREATED,
        )