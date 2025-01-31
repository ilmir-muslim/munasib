import asyncio
from datetime import datetime
from aiogram import Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.api_client import (
    check_worker_status,
    get_goods_list,
    get_operation_list,
    get_wokers_static_info,
    record_operation,
    works_done_today,
)
from src.kbds.inline_kb import (
    change_operation,
    choose_date,
    choose_goods,
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
    print(f"Operation ID str 45: {operation_id}")  # DEBUG
    operation_id = operation_id.replace("operation_", "")
    print(f"Operation ID str 46: {operation_id}, {type(operation_id)}")  # DEBUG
    try:
        operations = await get_operation_list()
        print(f"Operations строка 48: {operations}")  # DEBUG
        selected_operation = next(
            (op for op in operations if op["id"] == int(operation_id)), None
        )
        print(f"Selected operation str 52: {selected_operation}")  # DEBUG

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
    await state.update_data(state_data)

    try:
        if "quantity" not in state_data:
            await ask_quantity(callback_query, state)
            quantity = state_data["quantity"]
            quantity = int(quantity)
        else:
            quantity = state_data["quantity"]
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
        good_id = state_data.get("good_id", None)
        await record_operation(
            telegram_id=telegram_id,
            operation_id=operation_id,
            quantity=quantity,
            date=date,
            goods_id=good_id,
        )
        logging.info(
            f"Operation recorded: {operation_id}, {quantity}, {date}, {good_id}"
        )
    else:
        await record_operation(
            telegram_id=telegram_id,
            operation_id=operation_id,
            quantity=quantity,
            date=date,
        )
        logging.info(f"Operation recorded: {operation_id}, {quantity}, {date}")

    await callback_query.message.delete()
    await update_status(callback_query, state, new_msg=True)


async def settings_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик настроек."""
    user_id = callback_query.from_user.id
    state_data = await state.get_data()
    add_goods = state_data.get("add_goods", False)
    kb = await settings(user_id, add_goods)
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


async def handle_change_good(callback_query: types.CallbackQuery):
    """Обработчик выбора товара."""
    kb = await choose_goods()
    await callback_query.message.edit_reply_markup(reply_markup=kb)


async def handle_select_good(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик выбора товара."""
    good_id = callback_query.data
    print(f"Operation ID str 86: {good_id}")  # DEBUG
    good_id = good_id.replace("good_", "")
    try:
        goods = await get_goods_list()
        selected_good = next(
            (good for good in goods if good["id"] == int(good_id)), None
        )
        print(f"Selected operation str 90: {selected_good}")  # DEBUG

        if selected_good:
            # Обновляем состояние

            await state.update_data({"selected_good": selected_good})
            # Возврат к статусу после выбора
            await update_status(callback_query, state)
        else:
            await callback_query.answer("Товар не найден.", show_alert=True)
    except Exception as e:
        print(f"Error handling operation selection: {e}")


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
        operations = await get_operation_list()
        goods_list = await get_goods_list()

        selected_operation = state_data.get("selected_operation", None)
        selected_date = state_data.get("selected_date", date)
        print(f"Goods list строка 186: {goods_list}")  # DEBUG
        selected_good = state_data.get("selected_good", None)


        if not selected_operation:
            # Получение операции по умолчанию
            worker_static_info = await get_wokers_static_info(user_id)
            worker_data = (
                worker_static_info if isinstance(worker_static_info, list) else []
            )
            if not worker_data:
                raise ValueError(
                    f"Ошибка: worker_static_info['data'] пуст для user_id={user_id}"
                )
            worker_static_info = worker_data[0]

            default_operation_id = worker_static_info["default_operation"]

            if not isinstance(operations, list):
                raise TypeError(
                    f"Ошибка: get_operation_list() вернул {type(operations)}, ожидался список"
                )

            selected_operation = next(
                (op for op in operations if op["id"] == default_operation_id), None
            )
            if not selected_operation:
                raise ValueError(
                    f"Ошибка: операция с ID {default_operation_id} не найдена"
                )
            await state.update_data({"selected_operation": selected_operation})
            print(f"Default operation ID 186: {default_operation_id}")
            operations = await get_operation_list()
            if not operations:
                raise ValueError("Ошибка: список операций пуст")
            selected_operation = next(
                (op for op in operations if op["id"] == default_operation_id), None
            )
            if not selected_operation:
                raise ValueError(
                    f"Ошибка: операция с ID {default_operation_id} не найдена"
                )
        else:
            # Получаем данные из состояния
            current_operation_name = selected_operation["name"]
            print(f"Current operation name from state: {current_operation_name}")
            print(f"Current state_data строка 194: {state_data}")  # DEBUG
        if selected_operation:
            current_operation_name = selected_operation["name"]
        else:
            current_operation_name = "Операция не выбрана"
        
        add_goods = selected_operation["add_goods"]
        await state.update_data({"add_goods": add_goods})
        if add_goods:
            if selected_good is None:
                selected_good_name = goods_list[0]["name"]
                good_id = goods_list[0]["id"]
                await state.update_data({"good_id": good_id})
            else:
                selected_good_name = selected_good["name"]
                good_id = selected_good["id"]
                await state.update_data({"good_id": good_id})
        else:
            selected_good_name = None

        status_message_args = {
            "status": status,
            "current_operation_name": current_operation_name,
            "works_done": works_done,
            "selected_date": selected_date,
            "add_goods": add_goods,
        }
        if selected_good_name is not None:
            status_message_args["selected_good_name"] = selected_good_name

        final_output = await status_message(**status_message_args)
        print(f"Final output строка 273: {final_output}")  # DEBUG
        await state.update_data({"final_output": final_output})

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
    await callback_query.message.delete()
    while True:
        try:
            await update_status(callback_query, state, new_msg=True)
            await asyncio.sleep(600)
        except Exception as e:
            print(f"Error during status window: {e}")


async def handle_go_back(callback_query: types.CallbackQuery, state: FSMContext):
    """Возврат к окну статуса."""
    await callback_query.message.delete()
    await update_status(callback_query, state, new_msg=True)


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
    dp.callback_query.register(
        handle_operation_selection, lambda c: c.data.startswith("operation_")
    )
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
    dp.callback_query.register(handle_change_good, lambda c: c.data == "choose_goods")
    dp.callback_query.register(handle_select_good, lambda c: c.data.startswith("good_"))
