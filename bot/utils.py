import aiohttp

API_BASE_URL = "http://127.0.0.1:8000/api"  # Обратите внимание на добавление "/api" к URL

async def fetch_tubeteikas():
    """Получение списка тюбетеек из API."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/tubeteikas/") as response:
            if response.status == 200:
                return await response.json()
            else:
                # Обработка ошибок, если что-то пошло не так
                return []
