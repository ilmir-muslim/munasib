import asyncio
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.api_client import (
    check_worker_status,
    get_default_operation,
    get_goods_list,
    get_operation_list,
    get_wokers_static_info,
    record_operation,
    works_done_today,
)
from src.kbds.inline_kb import (
    change_operation,
    choose_date,
    confirm_quantity,
    main_menu,
    settings,
    start_work_button,
)
from src.messages.messages import status_message

import logging


class QuantityState(StatesGroup):
    waiting_for_quantity = State()
    waiting_for_date = State()


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

            await state.update_data({"selected_operation": selected_operation})
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
    current_data = await state.get_data()
    await state.update_data(current_data)
    # Переходим в состояние ожидания ввода количества
    await state.set_state(QuantityState.waiting_for_quantity)


async def save_quantity_to_state(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)


async def add_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    print(f"str state_data 127 {state_data}")

    quantity = state_data["quantity"]

    try:
        quantity = int(quantity)
    except ValueError:
        await callback_query.message.reply(
            "Пожалуйста, введите корректное числовое значение."
        )
        return

    telegram_id = callback_query.from_user.id

    operation_id = state_data["selected_operation"]["id"]
    print(f"str 98 {operation_id}")

    if not operation_id:
        print("Операция не найдена. str 127")
        return
    current_date = datetime.now().date()
    date = state_data.get("selected_date", current_date.isoformat())

    workers_data = await get_wokers_static_info(telegram_id)
    worker = next((w for w in workers_data if w["telegram_id"] == telegram_id), None)
    edit_goods = worker["edit_goods"]

    if edit_goods:
    # Записываем операцию
        good_id = state_data.get("item_id", None)
        await record_operation(
            telegram_id=telegram_id, operation_id=operation_id, quantity=quantity, date=date, goods_id=good_id
        )
        logging.info(f"Operation recorded: {operation_id}, {quantity}, {date}, {good_id}")
    else:
        await record_operation(
            telegram_id=telegram_id, operation_id=operation_id, quantity=quantity, date=date
        )
        logging.info(f"Operation recorded: {operation_id}, {quantity}, {date}")

    await callback_query.message.delete()
    await update_status(callback_query, state, new_msg=True)


async def settings_handler(callback_query: types.CallbackQuery):
    """Обработчик настроек."""
    user_id = callback_query.from_user.id
    kb = await settings(user_id)
    await callback_query.message.edit_reply_markup(reply_markup=kb)


async def handle_change_date(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик изменения даты."""
    kb = await choose_date()
    await callback_query.message.edit_reply_markup(reply_markup=kb)
    current_data = await state.get_data()
    await state.update_data(current_data)
    await state.set_state(QuantityState.waiting_for_date)


async def handle_select_date(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик выбора даты."""
    date = callback_query.data
    await state.update_data({"selected_date": date})
    await update_status(callback_query, state)

async def handle_select_good(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик выбора товара."""
    good_id = callback_query.data
    await state.update_data({"selected_good": good_id})
    await update_status(callback_query, state)


async def update_status(
    callback_query: types.CallbackQuery, state: FSMContext, new_msg=False, date=None
):
    """Обновляет окно статуса для пользователя."""

    if date is None:
        date = datetime.now().date()

    try:
        user_id = callback_query.from_user.id
        status = await check_worker_status(user_id)
        works_done = await works_done_today(user_id)
        state_data = await state.get_data()


        selected_operation = state_data.get("selected_operation", None)
        selected_date = state_data.get("selected_date", date)
        goods_list = await get_goods_list()
        selected_item = state_data.get("selected_item", None)

        if selected_item is None:
            selected_item = goods_list[0]["name"]
            item_id = goods_list[0]["id"]
            await state.update_data({"item_id": item_id})

        if not selected_operation:
            # Получение операции по умолчанию
            default_operation = await get_default_operation(user_id)
            print(f"Default operation: {default_operation}")  # DEBUG
            if default_operation:
                await state.update_data({"selected_operation": default_operation})
                current_operation_name = default_operation["name"]
                print(f"Current operation name from state: {current_operation_name}")
            else:
                current_operation_name = "Операция не задана"
        else:
            # Получаем данные из состояния
            current_operation_name = selected_operation["name"]
            print(f"Current operation name from state: {current_operation_name}")
            print(f"Current state_data строка 194: {state_data}")  # DEBUG

        final_output = await status_message(
            status=status,
            current_operation_name=current_operation_name,
            works_done=works_done,
            selected_date=selected_date,
            user_id=user_id,
            selected_item=selected_item,
        )

        kb = await main_menu()

        if new_msg:
            await callback_query.message.answer(
                text=final_output, reply_markup=kb, parse_mode="HTML"
            )
        else:
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
    dp.callback_query.register(
        handle_change_operation, lambda c: c.data == "change_operation"
    )
    dp.callback_query.register(handle_operation_selection, lambda c: c.data.isdigit())
    dp.callback_query.register(handle_go_back, lambda c: c.data == "go_back")
    dp.callback_query.register(end_work, lambda c: c.data == "end_work")
    dp.callback_query.register(ask_quantity, lambda c: c.data == "add_quantity")
    dp.message.register(save_quantity_to_state, QuantityState.waiting_for_quantity)
    dp.callback_query.register(add_quantity, lambda c: c.data == "confirm")
    dp.callback_query.register(settings_handler, lambda c: c.data == "settings")
    dp.callback_query.register(
        handle_change_date, lambda c: c.data.startswith("change_date")
    )
    dp.callback_query.register(handle_select_date, QuantityState.waiting_for_date)
    dp.callback_query.register(status_window, lambda c: c.data == "start_work")
    dp.callback_query.register(handle_select_good, lambda c: c.data == "choose_goods")