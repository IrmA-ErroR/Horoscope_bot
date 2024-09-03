from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import config
import functions  # Импортируем функции, связанные с гороскопами

async def handle_callback(callback_query: types.CallbackQuery, state: FSMContext):
    action = callback_query.data
    
    if action == "daily":
        # Ваш код для получения прогноза на день
        await callback_query.message.answer("Вот ваш прогноз на сегодня...")
    
    elif action == "weekly":
        # Ваш код для получения прогноза на неделю
        await callback_query.message.answer("Вот ваш прогноз на неделю...")
    
    elif action == "monthly":
        # Ваш код для получения прогноза на месяц
        await callback_query.message.answer("Вот ваш прогноз на месяц...")
    
    elif action == "menu":
        # Ваш код для возврата в главное меню
        await callback_query.message.answer("Вы вернулись в главное меню.")
    
    # Обязательно завершаем обработку callback запроса
    await callback_query.answer()
