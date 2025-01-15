from aiogram.utils.keyboard import ReplyKeyboardBuilder

keyboard = ReplyKeyboardBuilder()

keyboard.button(text="ввод количества работ")
keyboard.button(text="сменить операцию")
keyboard.button(text="получить зп")
keyboard.button(text="завершить работу")
