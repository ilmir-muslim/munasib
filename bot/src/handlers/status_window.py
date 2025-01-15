import asyncio
from aiogram import Dispatcher, types

from src.kbds.inline_kb import change_operation, main_menu
from src.utils import check_worker_status, works_done_today


async def status_window(callback_query: types.CallbackQuery):
    """Обработчик получения статуса."""
    user_id = callback_query.from_user.id
    message_old = ""

    while True:
        # Получаем статус пользователя и выполненные операции
        status = await check_worker_status(user_id)
        works_done = await works_done_today(user_id)

        # Формируем отформатированное сообщение
        final_output = (
            "<b>🔍 Your Current Status:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            "<b>📋 Operations Completed Today:</b>\n"
            f"<b>{works_done}</b>"
        )

        # Проверяем изменения в тексте
        if message_old == final_output:
            await asyncio.sleep(10)
            continue
        print(final_output)

        try:
            # Получаем клавиатуру
            keyboard = await main_menu()

            # Отправляем сообщение
            await callback_query.message.answer(
                text=final_output, reply_markup=keyboard, parse_mode="HTML"
            )
            message_old = final_output
        except Exception as e:
            print(f"Error during status window: {e}")
            break
        await asyncio.sleep(10)




async def handle_change_operation(callback_query: types.CallbackQuery):
    """Обработчик для смены операции."""
    keyboard = await change_operation()
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)

async def handle_go_back(callback_query: types.CallbackQuery):
    """Возврат к окну статуса."""
    await status_window(callback_query)


def register_status(dp: Dispatcher):
    dp.callback_query.register(status_window, lambda c: c.data == "start_work")
    dp.callback_query.register(handle_change_operation, lambda c: c.data == "change_operation")
    dp.callback_query.register(lambda c: c.data == "go_back")