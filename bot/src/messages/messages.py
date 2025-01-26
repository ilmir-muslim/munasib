from src.api_client import get_wokers_static_info


async def status_message(status, current_operation_name, works_done, selected_date, user_id,selected_item=None):
    workers_data = await get_wokers_static_info(user_id)
    worker = next((w for w in workers_data if w["telegram_id"] == user_id), None)
    edit_goods = worker["edit_goods"]

    if edit_goods:
        final_output = (
        "<b>🔍 Твой текущий статус:</b>\n"
        f"<b><i>{status}</i></b>\n\n"
        "<b>🔧 Текущая операция:</b>\n"
        f"<b>{current_operation_name}</b>\n\n"
        "<b>📋 Сделано операций за сегодня:</b>\n"
        f"<b>{works_done}</b>\n\n"
        "<b>📦 Выбранный товар:</b>\n"
        f"<b>{selected_item}</b>\n\n"
        "<b>дата записи</b>\n"
        f"<b>{selected_date}</b>"
            )
    else:
        final_output = (
            "<b>🔍 Твой текущий статус:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            "<b>🔧 Текущая операция:</b>\n"
            f"<b>{current_operation_name}</b>\n\n"
            "<b>📋 Сделано операций за сегодня:</b>\n"
            f"<b>{works_done}</b>\n\n"
            "<b>дата записи</b>\n"
            f"<b>{selected_date}</b>"
                )
        
    return final_output