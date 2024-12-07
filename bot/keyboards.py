from aiogram import types


def work_place_keyboard():
    """Создание клавиатуры для выбора места работы."""
    buttons = [
        [types.InlineKeyboardButton(text="Таркиб", callback_data="work_place_tarkib")],
        [types.InlineKeyboardButton(text="Тадрис", callback_data="work_place_tadris")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def language_keyboard():
    """Создание клавиатуры для выбора языка."""
    buttons = [
        [types.InlineKeyboardButton(text="عربية", callback_data="language_ar")],
        [types.InlineKeyboardButton(text="Русский", callback_data="language_ru")],
        [types.InlineKeyboardButton(text="English", callback_data="language_en")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
