import aiohttp


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
    async with aiohttp.ClientSession() as session:
        async with session.get("http://127.0.0.1:8000/worker_api/positions/") as response:
            if response.status == 200:
                data = await response.json()
                return [{"id": pos["id"], "name": pos["name"]} for pos in data.get("positions", [])]
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


    