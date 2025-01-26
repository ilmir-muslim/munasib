import logging

from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admins_panel.models import (
    Goods,
    Operation,
    OperationLog,
    Position,
    Worker,
)
from admins_panel.views import OperationLogListView
from worker_api.serializers import PositionSerializer

logger = logging.getLogger("custom_logger")


class CheckTelegramIdView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            Worker.objects.get(telegram_id=telegram_id)
            return Response({"exists": True})
        except Worker.DoesNotExist:
            return Response({"exists": False})


class RegisterNewUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Извлечение данных из запроса
        name = request.data.get("name")
        position_id = request.data.get("position_id")
        telegram_id = request.data.get("telegram_id")

        # Валидация входных данных
        if not all([name, position_id, telegram_id]):
            return Response(
                {"error": "name, position_id, and telegram_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Создание нового пользователя
        Worker.objects.create(
            name=name, position_id=position_id, telegram_id=telegram_id
        )

        # Ответ пользователю
        return Response(
            {"message": "User successfully registered."},
            status=status.HTTP_201_CREATED,
        )


class CheckAdminsRightsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            worker = Worker.objects.get(telegram_id=telegram_id)
            return Response({"admins_rights": worker.position.admins_rights})

        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=404)
        except Position.DoesNotExist:
            return Response({"error": "Position not found"}, status=404)


class Positions(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.info("Fetching positions from database")

        positions = Position.objects.select_related("default_operation").all()
        serializer = PositionSerializer(positions, many=True)
        logger.debug(f"Found {positions.count()} positions")
        return Response({"positions": serializer.data})


class StatusWindowView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        try:
            worker = Worker.objects.get(telegram_id=telegram_id)
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

    def get(self, request, telegram_id):
        try:
            worker = Worker.objects.get(telegram_id=telegram_id)
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


class WorkersStaticInfo(APIView):
    permission_classes = [AllowAny]

    def get(self, request, telegram_id):
        workers = Worker.objects.filter(telegram_id=telegram_id)
        return Response(
            {
                "workers": [
                    {
                        "id": worker.id,
                        "telegram_id": worker.telegram_id,
                        "name": worker.name,
                        "position": worker.position.name,
                        "admin_rights": worker.position.admins_rights,
                        "edit_goods": worker.position.edit_goods,
                    }
                    for worker in workers
                ]
            }
        )


class OperationList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        operations = Operation.objects.all()
        return Response(
            {
                "operations": [
                    {
                        "id": operation.id,
                        "name": operation.name,
                        "price": operation.price,
                        "add_goods": operation.add_goods,
                    }
                    for operation in operations
                ]
            }
        )


class GoodsList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        goods = Goods.objects.all()
        return Response(
            {
                "goods": [
                    {"id": good.id, "name": good.name, "price": good.price}
                    for good in goods
                ]
            }
        )


class BotOperationLogListView(OperationLogListView):
    template_name = "worker_api/bot_operation_log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавить любой специфичный контекст для бота, если нужно
        context["restricted_access"] = True
        return context


class RecordOperationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Извлечение данных из запроса
        telegram_id = request.data.get("telegram_id")
        operation_id = request.data.get("operation_id")
        quantity = request.data.get("quantity")
        date = request.data.get("date")
        goods_id = request.data.get("goods_id")

        # Валидация входных данных
        if not all([telegram_id, operation_id, quantity]):
            return Response(
                {"error": "worker_id, operation_id, and quantity are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        quantity = int(quantity)
        worker = Worker.objects.get(telegram_id=telegram_id)
        operation = Operation.objects.get(id=operation_id)
        goods = Goods.objects.get(id=goods_id)
        # Создание записи OperationLog
        OperationLog.objects.create(
            worker=worker, operation=operation, goods=goods, quantity=quantity, date=date
        )
        # Ответ пользователю
        return Response(
            {"message": "Operation successfully recorded."},
            status=status.HTTP_201_CREATED,
        )
