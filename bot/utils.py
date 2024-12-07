from sqlalchemy import select
from database import database, workers


async def check_user_exists(user_id: int) -> bool:
    query = select(workers.c.id_telegram).where(workers.c.id_telegram == str(user_id))
    result = await database.fetch_one(query)
    return result is not None


async def register_user(name: str, work_place: str, id_telegram: int, language: str):
    query = workers.insert().values(
        name=name,
        work_place=work_place,
        id_telegram=str(id_telegram),
        language=language,
    )
    await database.execute(query)


async def get_user_language(user_id: int) -> str:
    query = select(workers.c.language).where(workers.c.id_telegram == str(user_id))
    result = await database.fetch_one(query)
    return result["language"] if result else "en"  # По умолчанию возвращаем 'en'
