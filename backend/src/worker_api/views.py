import logging

from django.utils.timezone import now
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admins_panel.models import Operation, OperationLog, Position, Worker
from worker_api.serializers import PositionSerializer

logger = logging.getLogger("custom_logger")

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
            raise NotFound(
                {"error": f"Operation with id {operation_id} not found."}
            ) from exc

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
        position_id = request.data.get("position_id")
        id_telegram = request.data.get("id_telegram")

        # Валидация входных данных
        if not all([name, position_id, id_telegram]):
            return Response(
                {"error": "name, position_id, and id_telegram are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создание нового пользователя
        Worker.objects.create(
            name=name, position_id=position_id, id_telegram=id_telegram
        )

        # Ответ пользователю
        return Response(
            {"message": "User successfully registered."},
            status=status.HTTP_201_CREATED,
        )


class CheckAdminsRightsView(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def get(self, request, id_telegram):
        try:
            worker = Worker.objects.get(id_telegram=id_telegram)
            return Response({"admins_rights": worker.position.admins_rights})

        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=404)
        except Position.DoesNotExist:
            return Response({"error": "Position not found"}, status=404)


class Positions(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def get(self, request):
        logger.info("Fetching positions from database")

        positions = Position.objects.select_related ('default_operation').all()
        serializer = PositionSerializer(positions, many=True)
        logger.debug(f"Found {positions.count()} positions")
        return Response({"positions": serializer.data})


class StatusWindowView(APIView):
    permission_classes = [AllowAny]  # Позволяет доступ без авторизации

    def get(self, request, id_telegram):
        try:
            worker = Worker.objects.get(id_telegram=id_telegram)
            user_status = {
                "Работник": worker.name,
                "должность": worker.position.name,
                "зарплата": worker.salary,
            }
            
            print(user_status)
            return Response({"user_status": user_status})

        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=404)


class WorksDoneToday(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id_telegram):
        try:
            worker = Worker.objects.get(id_telegram=id_telegram)
            works_done = OperationLog.objects.filter(
                worker=worker, date__date=now().date()
            )
            print(
                {
                    "works_done": [
                        {
                            "operation": work_done.operation.name,
                            "quantity": work_done.quantity,
                        }
                        for work_done in works_done
                    ]
                }
            )
            return Response(
                {
                    "works_done": [
                        {
                            "operation": work_done.operation.name,
                            "quantity": work_done.quantity,
                        }
                        for work_done in works_done
                    ]
                }
            )

        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=404)

class OperationList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        operations = Operation.objects.all()
        return Response(
            {
                "operations": [
                    {"id": operation.id, "name": operation.name, "price": operation.price} for operation in operations
                ]
            }
        )