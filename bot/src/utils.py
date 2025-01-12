import aiohttp


async def check_user_exists(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/api/worker_api/check_telegram_id/{user_id}/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('exists', False)
            return False

async def register_user(name: str, work_place: str, id_telegram: int):
    async with aiohttp.ClientSession() as session:
        payload = {
            'name': name,
            'work_place': work_place,
            'id_telegram': id_telegram
        }
        async with session.post(
            "http://127.0.0.1:8000/api/worker_api/register_user/", json=payload
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data
            return None

async def check_admins_rights(user_id: int) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://127.0.0.1:8000/api/worker_api/check_admins_rights/{user_id}/"
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("admins_rights", False)
            return False
