import json
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.utils import check_user_exists, register_user, get_user_language
from bot.keyboards import work_place_keyboard, language_keyboard


class RegisterStates(StatesGroup):
    waiting_for_language = State()
    waiting_for_password = State()
    waiting_for_name = State()
    waiting_for_work_place = State()


# Загрузка переводов
def load_translations(lang_code):
    with open(f"locales/{lang_code}.json", "r", encoding="utf-8") as file:
        return json.load(file)


async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start."""
    user_id = message.from_user.id

    if await check_user_exists(user_id):
        language = await get_user_language(user_id)
        translations = load_translations(language)
        await message.answer(translations["welcome_back"])
    else:
        await message.answer("Language / Язык / لغة", reply_markup=language_keyboard())
        await state.set_state(RegisterStates.waiting_for_language)


async def language_received(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик получения языка."""
    language = callback_query.data.split("_")[1]
    translations = load_translations(language)
    await state.update_data(language=language)

    await callback_query.message.answer(translations["enter_password"])
    await state.set_state(RegisterStates.waiting_for_password)


async def password_received(message: types.Message, state: FSMContext):
    """Обработчик получения пароля."""
    data = await state.get_data()
    translations = load_translations(data["language"])
    CORRECT_PASSWORD = "YOUR_PASSWORD"  # Замените на реальный пароль

    if message.text != CORRECT_PASSWORD:
        await message.answer(translations["incorrect_password"])
        return

    await state.update_data(password=message.text)
    await message.answer(translations["enter_name"])
    await state.set_state(RegisterStates.waiting_for_name)


async def name_received(message: types.Message, state: FSMContext):
    """Обработчик получения имени."""
    data = await state.get_data()
    translations = load_translations(data["language"])

    await state.update_data(name=message.text)
    await message.answer(
        translations["select_work_place"], reply_markup=work_place_keyboard()
    )
    await state.set_state(RegisterStates.waiting_for_work_place)


async def work_place_received(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработчик получения места работы."""
    data = await state.get_data()
    translations = load_translations(data["language"])

    await state.update_data(work_place=callback_query.data.split("_")[2])
    data = (
        await state.get_data()
    )  # Обновляем данные состояния после добавления work_place

    try:
        await register_user(
            name=data["name"],
            work_place=data["work_place"],
            id_telegram=callback_query.from_user.id,
            language=data["language"],
        )
        await callback_query.message.answer(translations["registration_completed"])
    except Exception as e:
        await callback_query.message.answer(translations["registration_failed"])
        print(f"Error during registration: {e}")
    finally:
        await state.clear()


def register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command("start"))
    dp.callback_query.register(language_received, RegisterStates.waiting_for_language)
    dp.message.register(password_received, RegisterStates.waiting_for_password)
    dp.message.register(name_received, RegisterStates.waiting_for_name)
    dp.callback_query.register(
        work_place_received, RegisterStates.waiting_for_work_place
    )
