from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import functions
import user

from config import config
import functions  
from keyboard import create_forecast_keyboard

async def handle_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await user.get_user(user_id)
    day, month = map(int, user_data[3].split('.'))
    
    # Получаем номер знака зодиака 
    zodiac = functions.get_zodiac_sign(day, month)
    zodiac_sign = int(zodiac[1])

    if zodiac_sign is None:
        await callback_query.message.answer("Не удалось определить ваш знак зодиака. Пожалуйста, введите дату рождения.")
        return
    
    action = callback_query.data

    if action == "daily":
        horoscope = functions.get_horoscope_by_day(zodiac_sign, "today")
        await callback_query.message.answer(f"Вот ваш прогноз на сегодня:\n\n{horoscope}", reply_markup=create_forecast_keyboard())
    
    elif action == "weekly":
        horoscope = functions.get_horoscope_by_week(zodiac_sign)
        await callback_query.message.answer(f"Вот ваш прогноз на неделю:\n\n{horoscope}", reply_markup=create_forecast_keyboard())
    
    
    elif action == "monthly":
        horoscope = functions.get_horoscope_by_month(zodiac_sign)
        await callback_query.message.answer(f"Вот ваш прогноз на месяц:\n\n{horoscope}", reply_markup=create_forecast_keyboard())
        
    # elif action == "menu":
    #     await callback_query.message.answer("Вы вернулись в главное меню.")
    
    # Завершаем обработку callback запроса
    await callback_query.answer()
