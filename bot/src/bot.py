import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.handlers.start_handler import register_start
from src.handlers.worker_ui import register_status


# Загрузка переменных окружения
load_dotenv(find_dotenv())

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
register_start(dp)
register_status(dp)


async def main():
    """Главная функция запуска бота."""
    await bot.delete_webhook(
        drop_pending_updates=True
    )  # Удаление вебхуков и очистка очереди
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
