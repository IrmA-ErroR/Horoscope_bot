from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_forecast_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="Прогноз на сегодня", callback_data="daily_forecast")
        ], 
        [
            InlineKeyboardButton(text="Прогноз на неделю", callback_data="weekly_forecast"),
            InlineKeyboardButton(text="Прогноз на месяц", callback_data="monthly_forecast")
        ],
        [
            InlineKeyboardButton(text="Меню", callback_data="menu")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
