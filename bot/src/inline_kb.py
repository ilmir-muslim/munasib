from aiogram import types

from src.utils import check_worker_status, get_positions


async def position_keyboard():
    """Создание динамической клавиатуры для выбора места работы."""
    positions = await get_positions()
    buttons = [
        [types.InlineKeyboardButton(text=pos["name"], callback_data=f"position_{pos['id']}")]
        for pos in positions
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


async def start_work_button():
    button = [
        [types.InlineKeyboardButton(text="Start Work", callback_data="start_work")]
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=button)
