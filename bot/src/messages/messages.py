
async def status_message(
    status,
    current_operation_name,
    works_done,
    selected_date,
    add_goods,
    selected_good_name=None,
):

    if add_goods:
        final_output = (
            "<b>🔍 حالتك الحالية:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            "<b>🔧 العملية الحالية:</b>\n"
            f"<b>{current_operation_name}</b>\n\n"
            "<b>📋 العمليات المنجزة اليوم:</b>\n"
            f"<b>{works_done}</b>\n\n"
            "<b>📦 المنتج المحدد:</b>\n"
            f"<b>{selected_good_name}</b>\n\n"
            "<b>📅 تاريخ التسجيل:</b>\n"
            f"<b>{selected_date}</b>"
        )
    else:
        final_output = (
            "<b>🔍 حالتك الحالية:</b>\n"
            f"<b><i>{status}</i></b>\n\n"
            "<b>🔧 العملية الحالية:</b>\n"
            f"<b>{current_operation_name}</b>\n\n"
            "<b>📋 العمليات المنجزة اليوم:</b>\n"
            f"<b>{works_done}</b>\n\n"
            "<b>📅 تاريخ التسجيل:</b>\n"
            f"<b>{selected_date}</b>"
        )

    return final_output
