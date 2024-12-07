from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    """Главное меню с кнопками."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/tubeteikas")],
            [KeyboardButton(text="/help")]
        ],
        resize_keyboard=True
    )
    return keyboard
