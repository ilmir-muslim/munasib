from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.kbds.inline_kb import position_keyboard, start_work_button
from src.utils import (
    check_admins_rights,
    check_user_exists,
    register_user,
)


class RegisterStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_name = State()
    waiting_for_position = State()


async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start."""
    user_id = message.from_user.id

    if await check_user_exists(user_id):
        admin_rights = await check_admins_rights(user_id)
        await message.answer("Welcome back!")
        if admin_rights:
            await message.answer("Your admin link is http://127.0.0.1:8000/admin")
        button = await start_work_button()
        await message.answer("Click the button to start work:", reply_markup=button)

    else:
        await message.answer("Please enter the password:")
        await state.set_state(RegisterStates.waiting_for_password)


async def password_received(message: types.Message, state: FSMContext):
    """Обработчик получения пароля."""
    correct_password = "1"  # Замените на реальный пароль

    if message.text != correct_password:
        await message.answer("Incorrect password. Please try again.")
        return

    await state.update_data(password=message.text)
    await message.answer("Please enter your name:")
    await state.set_state(RegisterStates.waiting_for_name)


async def name_received(message: types.Message, state: FSMContext):
    """Обработчик получения имени."""
    await state.update_data(name=message.text)
    keyboard = await position_keyboard()
    await message.answer("Please select your work place:", reply_markup=keyboard)
    await state.set_state(RegisterStates.waiting_for_position)


async def position_received(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик получения места работы."""
    await state.update_data(position_id=callback_query.data.split("_")[1])
    data = await state.get_data()

    try:
        await register_user(
            name=data["name"],
            position_id=data["position_id"],
            id_telegram=callback_query.from_user.id,
        )
        await callback_query.message.answer("Registration completed successfully!")
        button = await start_work_button()
        await callback_query.message.answer(
            "Please select your work place:", reply_markup=button
        )

    except Exception as e:
        await callback_query.message.answer("Registration failed. Please try again.")
        print(f"Error during registration: {e}")
    finally:
        await state.clear()


    


def register_start(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(password_received, RegisterStates.waiting_for_password)
    dp.message.register(name_received, RegisterStates.waiting_for_name)
    dp.callback_query.register(position_received, RegisterStates.waiting_for_position)
    
