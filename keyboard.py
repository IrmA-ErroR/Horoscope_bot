from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_forecast_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Прогноз на сегодня", callback_data="daily")
        ], 
        [
            InlineKeyboardButton(text="Прогноз на неделю", callback_data="weekly"),
            InlineKeyboardButton(text="Прогноз на месяц", callback_data="monthly")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def menu_keyboard():
    menu_button = KeyboardButton(text="Меню")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(menu_button) 
    return keyboard

async def handle_menu_message(message: types.Message):
    # Отправляем клавиатуру с прогнозами
    await message.answer("Вы в главном меню. Выберите прогноз:", reply_markup=create_forecast_keyboard())
