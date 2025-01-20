import asyncio
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.api_client import (
    check_worker_status,
    get_default_operation,
    get_operation_list,
    record_operation,
    works_done_today,
)
from src.kbds.inline_kb import (
    change_operation,
    confirm_quantity,
    main_menu,
    start_work_button,
)


class QuantityState(StatesGroup):
    waiting_for_quantity = State()


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

        kb = await main_menu()
        await callback_query.message.edit_text(
            text=final_output, reply_markup=kb, parse_mode="HTML"
        )
    except Exception as e:
        print(f"Error updating status: {e}")


async def status_window(callback_query: types.CallbackQuery, state: FSMContext):
    while True:
        try:
            await update_status(callback_query, state)
            await asyncio.sleep(600)
        except Exception as e:
            print(f"Error during status window: {e}")


async def handle_change_operation(callback_query: types.CallbackQuery):
    """Обработчик для смены операции."""
    kb = await change_operation()
    await callback_query.message.edit_reply_markup(reply_markup=kb)


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


async def ask_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    """Запрашиваем у пользователя количество."""
    button = await confirm_quantity()
    await callback_query.message.edit_text(
        "Введите количество и нажмите подтвердить", reply_markup=button
    )
    # Переходим в состояние ожидания ввода количества
    await state.set_state(QuantityState.waiting_for_quantity)


async def save_quantity_to_state(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)


async def add_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    print(f"str 127 {state_data}")
    quantity = state_data["quantity"]

    try:
        quantity = int(quantity)
    except ValueError:
        await callback_query.message.reply(
            "Пожалуйста, введите корректное числовое значение."
        )
        return

    telegram_id = callback_query.from_user.id

    operation_id = state_data['selected_operation']["id"]
    print(f"str 127 {operation_id}")

    if not operation_id:
        print("Операция не найдена. str 127")
        return

    # Записываем операцию
    response = await record_operation(
        telegram_id=telegram_id, operation_id=operation_id, quantity=quantity
    )

    if response.get("success"):
        print("Операция успешно записана!")
    else:
        error_message = response.get("error", "Не удалось записать операцию.")
        print(f"Ошибка: {error_message} str 142")
    await update_status(callback_query, state)


async def handle_go_back(callback_query: types.CallbackQuery):
    """Возврат к окну статуса."""
    kb = await main_menu()
    await callback_query.message.edit_reply_markup(reply_markup=kb)


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
    dp.callback_query.register(handle_operation_selection, lambda c: c.data.isdigit())
    dp.callback_query.register(handle_go_back, lambda c: c.data == "go_back")
    dp.callback_query.register(end_work, lambda c: c.data == "end_work")
    dp.callback_query.register(ask_quantity, lambda c: c.data == "add_quantity")
    dp.message.register(save_quantity_to_state, QuantityState.waiting_for_quantity)
    dp.callback_query.register(add_quantity, lambda c: c.data == "confirm")
