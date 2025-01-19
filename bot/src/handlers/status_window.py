import asyncio
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from src.api_client import (
    check_worker_status,
    get_default_operation,
    get_operation_list,
    works_done_today,
)
from src.kbds.inline_kb import change_operation, main_menu, start_work_button


async def update_status(callback_query: types.CallbackQuery, state: FSMContext):
    """Обновляет окно статуса для пользователя."""
    try:
        user_id = callback_query.from_user.id
        status = await check_worker_status(user_id)
        works_done = await works_done_today(user_id)
        current_operation = await state.get_data()

        selected_operation = current_operation.get("selected_operation", None)

        if not selected_operation:
            # Получение операции по умолчанию
            default_operation = await get_default_operation(user_id)
            print(f"Default operation: {default_operation}")  # DEBUG
            if default_operation:
                await state.set_data({"selected_operation": default_operation})
                current_operation_name = default_operation["name"]
                print(f"Current operation name from state: {current_operation_name}")
            else:
                current_operation_name = "Операция не задана"
        else:
            # Получаем данные из состояния
            current_operation_name = selected_operation["name"]
            print(f"Current operation name from state: {current_operation_name}")
            print(f"Current operation строка 41: {current_operation}")  # DEBUG

        final_output = (
            "<b>🔍 Твой текущий статус:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            f"<b>🔧 Текущая операция:</b>\n"
            f"<b>{current_operation_name}</b>\n\n"
            "<b>📋 Сделано операций за сегодня:</b>\n"
            f"<b>{works_done}</b>"
        )

        keyboard = await main_menu()
        await callback_query.message.edit_text(
            text=final_output, reply_markup=keyboard, parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error updating status: {e}")


async def status_window(
    callback_query: types.CallbackQuery, state: FSMContext, break_flag=False
):
    while True:
        try:
            await update_status(callback_query, state)
            await asyncio.sleep(600)
        except Exception as e:
            print(f"Error during status window: {e}")

async def handle_change_operation(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Обработчик для смены операции."""
    keyboard = await change_operation()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


async def handle_operation_selection(
    callback_query: types.CallbackQuery, state: FSMContext
):
    """Обработчик выбора операции."""
    operation_id = callback_query.data  # Получаем ID операции из callback_data
    print(f"Operation ID str 86: {operation_id}")  # DEBUG
    try:
        operations = await get_operation_list()
        selected_operation = next(
            (op for op in operations if str(op["id"]) == operation_id), None
        )
        print(f"Selected operation str 90: {selected_operation}")  # DEBUG

        if selected_operation:
            # Обновляем состояние

            await state.set_data({"selected_operation": selected_operation})
            # Возврат к статусу после выбора
            await update_status(callback_query, state)
        else:
            await callback_query.answer("Операция не найдена.", show_alert=True)
    except Exception as e:
        print(f"Error handling operation selection: {e}")
        await callback_query.answer("Произошла ошибка.", show_alert=True)


async def handle_go_back(callback_query: types.CallbackQuery):
    """Возврат к окну статуса."""
    keyboard = await main_menu()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)


async def end_work(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик завершения работы."""
    await state.clear()
    button = await start_work_button()
    await callback_query.message.edit_text(
        "Чтобы начать работу, нажмите кнопку", reply_markup=button
    )


def register_status(dp: Dispatcher):
    dp.callback_query.register(status_window, lambda c: c.data == "start_work")
    dp.callback_query.register(
        handle_change_operation, lambda c: c.data == "change_operation"
    )
    dp.callback_query.register(handle_go_back, lambda c: c.data == "go_back")
    dp.callback_query.register(end_work, lambda c: c.data == "end_work")
    dp.callback_query.register(handle_operation_selection, lambda c: c.data.isdigit())
