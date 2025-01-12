import os
import logging
import asyncio
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.handlers import register_handlers


# Загрузка переменных окружения
load_dotenv(find_dotenv())

API_BASE_URL = "http://127.0.0.1:8000"

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Создание бота
bot = Bot(token=TOKEN)
bot.parse_mode = "HTML"  # Установка parse_mode через свойство

# Использование MemoryStorage для FSM
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Регистрация обработчиков
register_handlers(dp)


async def main():
    """Главная функция запуска бота."""
    await bot.delete_webhook(
        drop_pending_updates=True
    )  # Удаление вебхуков и очистка очереди
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
