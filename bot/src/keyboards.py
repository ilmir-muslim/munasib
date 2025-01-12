from aiogram import types


def work_place_keyboard():
    """Создание клавиатуры для выбора места работы."""
    buttons = [
        [types.InlineKeyboardButton(text="Таркиб", callback_data="work_place_tarkib")],
        [types.InlineKeyboardButton(text="Тадрис", callback_data="work_place_tadris")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
