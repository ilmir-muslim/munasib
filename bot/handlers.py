from aiogram import Dispatcher, types
from aiogram.filters import Command
from bot.utils import fetch_tubeteikas
from bot.keyboards import main_menu_keyboard

async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    await message.answer("Welcome! Use the menu below:", reply_markup=main_menu_keyboard())

async def cmd_tubeteikas(message: types.Message):
    """Обработчик команды /tubeteikas."""
    tubeteikas = await fetch_tubeteikas()
    if not tubeteikas:
        await message.answer("No tubeteikas found.")
        return

    for tubeteika in tubeteikas:
        msg = (
            f"<b>ID:</b> {tubeteika['id']}\n"
            f"<b>Name:</b> {tubeteika['name']}\n"
            f"<b>Produced:</b> {tubeteika['produced']}\n"
            f"<b>Sold:</b> {tubeteika['sold']}\n"
            f"<b>Price:</b> {tubeteika['price']}"
        )
        await message.answer(msg)

def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков команд."""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_tubeteikas, Command("tubeteikas"))
