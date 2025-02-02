from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.api_client import check_user_exists, register_user
from src.kbds.inline_kb import position_keyboard, start_work_button


class RegisterStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_name = State()
    waiting_for_position = State()


async def cmd_start(message: types.Message, state: FSMContext):
    """معالج الأمر /start."""
    user_id = message.from_user.id

    if await check_user_exists(user_id):
        await message.answer("مرحبًا بعودتك!")
        button = await start_work_button()
        await message.answer("اضغط على الزر لبدء العمل:", reply_markup=button)

    else:
        await message.answer("يرجى إدخال كلمة المرور:")
        await state.set_state(RegisterStates.waiting_for_password)


async def password_received(message: types.Message, state: FSMContext):
    """معالج استلام كلمة المرور."""
    correct_password = "1"  # استبدل بكلمة المرور الحقيقية

    if message.text != correct_password:
        await message.answer("كلمة المرور غير صحيحة. يرجى المحاولة مرة أخرى.")
        return

    await state.update_data(password=message.text)
    await message.answer("يرجى إدخال اسمك:")
    await state.set_state(RegisterStates.waiting_for_name)


async def name_received(message: types.Message, state: FSMContext):
    """معالج استلام الاسم."""
    await state.update_data(name=message.text)
    keyboard = await position_keyboard()
    await message.answer("يرجى اختيار مكان عملك:", reply_markup=keyboard)
    await state.set_state(RegisterStates.waiting_for_position)


async def position_received(callback_query: types.CallbackQuery, state: FSMContext):
    """معالج استلام مكان العمل."""
    await state.update_data(position_id=callback_query.data.split("_")[1])
    data = await state.get_data()

    try:
        await register_user(
            name=data["name"],
            position_id=data["position_id"],
            telegram_id=callback_query.from_user.id,
        )
        await callback_query.message.answer("تم التسجيل بنجاح!")
        button = await start_work_button()
        await callback_query.message.answer(
            "يرجى اختيار مكان عملك:", reply_markup=button
        )

    except Exception as e:
        await callback_query.message.answer("فشل التسجيل. يرجى المحاولة مرة أخرى.")
        print(f"خطأ أثناء التسجيل: {e}")
    finally:
        await state.clear()


def register_start(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(password_received, RegisterStates.waiting_for_password)
    dp.message.register(name_received, RegisterStates.waiting_for_name)
    dp.callback_query.register(position_received, RegisterStates.waiting_for_position)
