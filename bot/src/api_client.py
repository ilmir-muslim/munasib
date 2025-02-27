import aiohttp

from src.utils.cache_manager import CacheManager


async def check_user_exists(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://backend:8000/worker_api/check_telegram_id/{user_id}/") as response:
            print(f"Response status: {response.status}")
            if response.status == 200:
                data = await response.json()
                return data.get("exists", False)
            return False
        print(f"Failed to check user with id {user_id}")


async def register_user(name: str, position_id: int, telegram_id: int):
    async with aiohttp.ClientSession() as session:
        payload = {"name": name, "position_id": position_id, "telegram_id": telegram_id}
        print(payload)
        async with session.post("http://backend:8000/worker_api/register_user/", json=payload) as response:
            if response.status == 201:
                data = await response.json()
                return data
            return None


async def get_positions() -> list:
    cache_name = "positions_cache"
    cached_data = CacheManager.read_cache(cache_name)

    if cached_data:
        print("Positions fetched from cache")
        return cached_data

    async with aiohttp.ClientSession() as session:
        async with session.get("http://backend:8000/worker_api/positions/") as response:
            if response.status == 200:
                data = await response.json()
                positions = [
                    {
                        "id": pos["id"],
                        "name": pos["name"],
                        "default_operation": pos["default_operation"],
                    }
                    for pos in data.get("positions", [])
                ]
                CacheManager.write_cache(cache_name, positions)  # Сохранение в кэш
                print(
                    "Positions fetched from server and cached"
                )  # Отладочное сообщение
                return positions
            return []


async def check_admins_rights(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://backend:8000/worker_api/check_admins_rights/{user_id}/") as response:
            if response.status == 200:
                data = await response.json()
                return data.get("admins_rights", False)
            return False


async def get_wokers_static_info(user_id) -> list:
    cache_name = "wokers_static_info"
    cached_data = (
        CacheManager.read_cache(cache_name) or []
    )  # Инициализируем пустым списком, если None
    user_data = next(
        (item for item in cached_data if item["telegram_id"] == user_id), None
    )

    if user_data:
        print("Workers static info fetched from cache")
        return [user_data]

    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://backend:8000/worker_api/workers_static_info/{user_id}/") as response:
            if response.status == 200:
                data = await response.json()
                workers_static_info = [
                    {
                        "id": item["id"],
                        "telegram_id": item["telegram_id"],
                        "name": item["name"],
                        "position": item["position"],
                        "admin_rights": item["admin_rights"],
                        "default_operation": item["default_operation"],
                    }
                    for item in data.get("workers", [])
                ]
                for worker in workers_static_info:
                    if not any(
                        cached["telegram_id"] == worker["telegram_id"]
                        for cached in cached_data
                    ):
                        cached_data.append(worker)

                CacheManager.write_cache(cache_name, cached_data)
                print(
                    f"Worker static info for user_id {user_id} fetched from server and cached"
                )
                return [
                    worker
                    for worker in workers_static_info
                    if worker["telegram_id"] == user_id
                ]
            print(f"Failed to fetch worker static info for user_id {user_id}")
            return []


async def check_worker_status(user_id: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://backend:8000/worker_api/status_window/{user_id}/") as response:
            if response.status == 200:
                data = await response.json()
                user_status = data.get("user_status", {})  # Извлекаем вложенный словарь
                formatted_status = "\n".join(
                    f"{key.capitalize()}: {value}" for key, value in user_status.items()
                )
                return f"{formatted_status}"  # Форматируем полный вывод
            return "Worker not found or error occurred."


async def works_done_today(user_id: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://backend:8000/worker_api/works_done_today/{user_id}/") as response:
            if response.status == 200:
                data = await response.json()
                operation_sums = {}
                for work in data["works_done"]:
                    operation = work["operation"]
                    quantity = work["quantity"]
                    operation_sums[operation] = (
                        operation_sums.get(operation, 0) + quantity
                    )

                # Создание списка операций
                operations = [
                    {"operation": operation, "quantity": quantity}
                    for operation, quantity in operation_sums.items()
                ]

                # Форматирование операций
                formatted_operations = "\n".join(
                    f"{op['operation']}: {op['quantity']}" for op in operations
                )

                return formatted_operations  # Возвращаем текст
            return "No works done today."


async def get_operation_list():
    cache_name = "operations_cache"
    cached_data = CacheManager.read_cache(cache_name)

    if cached_data:
        print("Operations fetched from cache")  # Отладочное сообщение
        return cached_data

    async with aiohttp.ClientSession() as session:
        async with session.get("http://backend:8000/worker_api/operations/") as response:
            if response.status == 200:
                data = await response.json()
                operations = [
                    {
                        "id": op["id"],
                        "name": op["name"],
                        "price": op["price"],
                        "add_goods": op["add_goods"],
                    }
                    for op in data.get("operations", [])
                ]
                CacheManager.write_cache(cache_name, operations)  # Сохранение в кэш
                print(
                    "Operations fetched from server and cached"
                )  # Отладочное сообщение
                return operations
            return []



async def get_goods_list():
    cache_name = "goods_cache"
    cached_data = CacheManager.read_cache(cache_name)

    if cached_data:
        print("Goods fetched from cache")  # Отладочное сообщение
        return cached_data

    async with aiohttp.ClientSession() as session:
        async with session.get("http://backend:8000/worker_api/goods_list/") as response:
            if response.status == 200:
                data = await response.json()
                goods = [
                    {"id": good["id"], "name": good["name"], "price": good["price"]}
                    for good in data.get("goods", [])
                ]
                CacheManager.write_cache(cache_name, goods)
                print("Goods fetched from server and cached")
                return goods

async def record_operation(telegram_id: int, operation_id: int, quantity: int, date, goods_id: int = None) -> dict:
    """Отправка данных о выполненной операции."""
    async with aiohttp.ClientSession() as session:
        payload = {
            "telegram_id": telegram_id,
            "operation_id": operation_id,
            "quantity": quantity,
            "date": date,
        }
        if goods_id is not None:
            payload["goods_id"] = goods_id
        print(f"Payload 204: {payload}")
        async with session.post("http://backend:8000/worker_api/record_operation/", json=payload) as response:
            if response.status == 201:
                return {"success": True, "message": "Operation successfully recorded."}
            try:
                error_message = await response.json()
            except aiohttp.ContentTypeError:
                error_message = await response.text()
            return {"success": False, "error": error_message}
