from aiogram import types

from src.utils import get_positions


async def position_keyboard():
    """Создание динамической клавиатуры для выбора места работы."""
    positions = await get_positions()
    buttons = [
        [types.InlineKeyboardButton(text=pos["name"], callback_data=f"position_{pos['id']}")]
        for pos in positions
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
