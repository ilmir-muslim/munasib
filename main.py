import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import database
from crud import router as api_router
from bot.bot import main as start_bot

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    logger.info("Database connected")
    yield
    await database.disconnect()
    logger.info("Database disconnected")


app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api")


# Запуск FastAPI в асинхронной задаче
def start_fastapi():
    import uvicorn

    logger.info("Starting FastAPI")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    logger.info("FastAPI started")


# Главная функция запуска программы
async def main():
    try:
        # Запуск FastAPI в отдельном потоке
        fastapi_task = asyncio.create_task(asyncio.to_thread(start_fastapi))
        logger.info("FastAPI task created")

        # Запуск Telegram бота
        bot_task = asyncio.create_task(start_bot())
        logger.info("Bot task created")

        await asyncio.gather(fastapi_task, bot_task)
    except Exception as e:
        logger.error(f"Error running main tasks: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Main function executed")
    except Exception as e:
        logger.error(f"Failed to run main: {e}")
