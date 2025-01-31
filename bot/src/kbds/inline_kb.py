import calendar
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.api_client import (
    get_goods_list,
    get_operation_list,
    get_positions,
    get_wokers_static_info,
)


async def main_menu():
    """Генерация клавиатуры первого уровня меню."""
    # Создаём список кнопок
    buttons = [
        InlineKeyboardButton(text="Настройки", callback_data="settings"),
        InlineKeyboardButton(text="Внести количество", callback_data="add_quantity"),
        InlineKeyboardButton(text="Завершение работы", callback_data="end_work"),
    ]

    # Создаём клавиатуру с row_width=3
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    )
    return keyboard


async def position_keyboard():
    """Создание динамической клавиатуры для выбора места работы."""
    positions = await get_positions()
    buttons = [
        [InlineKeyboardButton(text=pos["name"], callback_data=f"position_{pos['id']}")]
        for pos in positions
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def start_work_button():
    button = [[InlineKeyboardButton(text="Start Work", callback_data="start_work")]]
    return InlineKeyboardMarkup(inline_keyboard=button)


async def settings(user_id: int):
    buttons = [
        InlineKeyboardButton(text="Сменить операцию", callback_data="change_operation"),
    ]
    workers_data = await get_wokers_static_info(user_id)
    worker = next((w for w in workers_data if w["telegram_id"] == user_id), None)
    # edit_goods_custom_version = worker["edit_goods_custom_version"]
    print(f"Worker str 26: {worker}")
    edit_goods = worker["edit_goods"]
    print(f"edit_goods str 29: {edit_goods}")
    # if edit_goods_custom_version:
    #     buttons.append(
    #         InlineKeyboardButton(text="Добавить товар", callback_data="edit_goods")
    #     )  # TODO прописать кастомное меню, если будет время(заказчик не просил)

    buttons.append(
        InlineKeyboardButton(text="изменить дату", callback_data="change_date")
    )
    worker_name = worker["name"]
    url = f"http://127.0.0.1:8000/worker_api/bot_operation_log/?start_date=&end_date=&operation=&worker={worker_name}"
    buttons.append(InlineKeyboardButton(text="журнал операций", url=url))

    if edit_goods:
        buttons.append(
            InlineKeyboardButton(text="выбрать товар", callback_data="choose_goods")
        )

    buttons.append(InlineKeyboardButton(text="назад", callback_data="go_back"))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    )

    return keyboard


async def choose_date():
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]

    buttons = [
        InlineKeyboardButton(
            text=str(day), callback_data=f"{year}-{month:02d}-{day:02d}"
        )
        for day in range(1, days_in_month + 1)
    ]
    buttons.append(InlineKeyboardButton(text="назад", callback_data="go_back"))
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[buttons[i : i + 5] for i in range(0, len(buttons), 5)]
    )

    return keyboard


async def change_operation():
    operations = await get_operation_list()
    buttons = [
        InlineKeyboardButton(text=operation["name"], callback_data=f"operation_{operation["id"]}")
        for operation in operations
    ]
    inline_keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="go_back")]
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard


async def choose_goods():
    goods_list = await get_goods_list()
    buttons = [
        InlineKeyboardButton(text=goods["name"], callback_data=f"good_ {goods["id"]}")
        for goods in goods_list
    ]

    inline_keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    inline_keyboard.append(
        [InlineKeyboardButton(text="Назад", callback_data="go_back")]
    )
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def confirm_quantity():
    buttons = [[InlineKeyboardButton(text="подтвердить", callback_data="confirm")]]
    buttons.append([InlineKeyboardButton(text="назад", callback_data="go_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
