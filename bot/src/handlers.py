from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.utils import check_user_exists, get_admin_list, register_user
from src.keyboards import work_place_keyboard


class RegisterStates(StatesGroup):
    waiting_for_password = State()
    waiting_for_name = State()
    waiting_for_work_place = State()


async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start."""
    user_id = message.from_user.id

    if await check_user_exists(user_id):
        admin_list = await get_admin_list()
        await message.answer("Welcome back!")
        if user_id in admin_list:
            await message.answer("Your admin link is http://127.0.0.1:8000/admin")
    else:
        await message.answer("Please enter the password:")
        await state.set_state(RegisterStates.waiting_for_password)


async def password_received(message: types.Message, state: FSMContext):
    """Обработчик получения пароля."""
    CORRECT_PASSWORD = "1"  # Замените на реальный пароль

    if message.text != CORRECT_PASSWORD:
        await message.answer("Incorrect password. Please try again.")
        return

    await state.update_data(password=message.text)
    await message.answer("Please enter your name:")
    await state.set_state(RegisterStates.waiting_for_name)


async def name_received(message: types.Message, state: FSMContext):
    """Обработчик получения имени."""
    await state.update_data(name=message.text)
    await message.answer("Please select your work place:", reply_markup=work_place_keyboard())
    await state.set_state(RegisterStates.waiting_for_work_place)


async def work_place_received(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик получения места работы."""
    await state.update_data(work_place=callback_query.data.split("_")[2])
    data = await state.get_data()  # Обновляем данные состояния после добавления work_place

    try:
        await register_user(
            name=data["name"],
            work_place=data["work_place"],
            id_telegram=callback_query.from_user.id,
        )
        await callback_query.message.answer("Registration completed successfully!")
    except Exception as e:
        await callback_query.message.answer("Registration failed. Please try again.")
        print(f"Error during registration: {e}")
    finally:
        await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(password_received, RegisterStates.waiting_for_password)
    dp.message.register(name_received, RegisterStates.waiting_for_name)
    dp.callback_query.register(work_place_received, RegisterStates.waiting_for_work_place)
