import asyncio
from aiogram import Dispatcher, types

from src.kbds.inline_kb import change_operation, main_menu
from src.utils import check_worker_status, works_done_today


async def update_status(callback_query: types.CallbackQuery):
    """Обновляет окно статуса для пользователя."""
    try:
        user_id = callback_query.from_user.id  # Извлекаем user_id из callback_query
        status = await check_worker_status(user_id)
        works_done = await works_done_today(user_id)

        final_output = (
            "<b>🔍 Твой текущий статус:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            "<b>📋 Сделано операций за сегодня:</b>\n"
            f"<b>{works_done}</b>"
        )

        keyboard = await main_menu()
        await callback_query.message.edit_text(text=final_output, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        print(f"Error updating status: {e}")

async def status_window(callback_query: types.CallbackQuery):
    """Обработчик получения статуса."""
    while True:
        try:
            await update_status(callback_query)
            await asyncio.sleep(600)
        except Exception as e:
            print(f"Error during status window: {e}")
            break


async def handle_change_operation(callback_query: types.CallbackQuery):
    """Обработчик для смены операции."""
    keyboard = await change_operation()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

async def handle_go_back(callback_query: types.CallbackQuery):
    """Возврат к окну статуса."""
    keyboard = await main_menu()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

async def end_work(callback_query: types.CallbackQuery):
    """Обработчик завершения работы."""

    await callback_query.message.answer("Работа завершена. До свидания!")


def register_status(dp: Dispatcher):
    dp.callback_query.register(status_window, lambda c: c.data == "start_work")
    dp.callback_query.register(handle_change_operation, lambda c: c.data == "change_operation")
    dp.callback_query.register(handle_go_back, lambda c: c.data == "go_back")