import aiohttp

from src.utils.cache_manager import CacheManager


async def check_user_exists(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/worker_api/check_telegram_id/{user_id}/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('exists', False)
            return False

async def register_user(name: str, position_id: int, id_telegram: int):
    async with aiohttp.ClientSession() as session:
        payload = {
            'name': name,
            'position_id': position_id,
            'id_telegram': id_telegram
        }
        print(payload)
        async with session.post(
            "http://127.0.0.1:8000/worker_api/register_user/", json=payload
        ) as response:
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
        async with session.get("http://127.0.0.1:8000/worker_api/positions/") as response:
            if response.status == 200:
                data = await response.json()
                positions = [{"id": pos["id"], "name": pos["name"], "default_operation": pos["default_operation"]} for pos in data.get("positions", [])]
                CacheManager.write_cache(cache_name, positions)  # Сохранение в кэш
                print("Positions fetched from server and cached") # Отладочное сообщение
                return positions
            return []


async def check_admins_rights(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/worker_api/check_admins_rights/{user_id}/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("admins_rights", False)
            return False


async def check_worker_status(user_id: int) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/worker_api/status_window/{user_id}/"
        ) as response:
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
        async with session.get(
            f"http://127.0.0.1:8000/worker_api/works_done_today/{user_id}/"
        ) as response:
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
                    f"{op['operation']}: {op['quantity']}"
                    for op in operations
                )

                return formatted_operations  # Возвращаем текст
            return "No works done today."
         

async def get_operation_list():
    cache_name = "operations_cache"
    cached_data = CacheManager.read_cache(cache_name)
    
    if cached_data:
        print("Operations fetched from cache") # Отладочное сообщение
        return cached_data

    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/worker_api/operations/") as response:
            if response.status == 200:
                data = await response.json()
                operations = [{"id": op["id"], "name": op["name"], "price": op["price"]} for op in data.get("operations", [])]
                CacheManager.write_cache(cache_name, operations)  # Сохранение в кэш
                print("Operations fetched from server and cached") # Отладочное сообщение
                return operations
            return []

async def get_default_operation(user_id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/worker_api/status_window/{user_id}/"
        ) as response:
            if response.status != 200:
                return None

            data = await response.json()
            user_status = data.get("user_status", {})
            position_name = user_status.get("должность")
            if not position_name:
                return None

    positions = await get_positions()
    print(f"Positions: {positions}") # Отладочное сообщение
    operations = await get_operation_list()
    print(f"Operations: {operations}") # Отладочное сообщение

    position = next((pos for pos in positions if pos["name"] == position_name), None)
    if not position:
        return None

    default_operation_id = position["default_operation"]
    operation = next((op for op in operations if op["id"] == default_operation_id), None)
    print(f"Default operation: {operation}") # Отладочное сообщение
    return operation
