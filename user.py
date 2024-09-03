import aiosqlite
from datetime import datetime
from aiogram import types
from aiogram.fsm.context import FSMContext

from main import AstroStates

from config import config
import functions
# import keyboard

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_forecast_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Прогноз на день", callback_data="daily_forecast"),
        InlineKeyboardButton(text="Прогноз на неделю", callback_data="weekly_forecast"),
        InlineKeyboardButton(text="Прогноз на месяц", callback_data="monthly_forecast"),
        InlineKeyboardButton(text="Меню", callback_data="menu")
    ]
    keyboard.add(*buttons)
    return keyboard






# Инициализация базы данных
async def initialize_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                birthdate TEXT,
                zodiac_sign TEXT,
                first_time TEXT NOT NULL,
                resent_time TEXT NOT NULL        
            )
        ''')
        await db.commit()

# Добавление нового пользователя в базу данных
async def add_user(user_id, full_name, username, birthdate, zodiac_sign):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.cursor()
        check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        check_user = await check_user.fetchone()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if check_user is None:
            await cursor.execute('''
                INSERT INTO users (user_id, full_name, username, birthdate, zodiac_sign, first_time, resent_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, full_name, username, birthdate, zodiac_sign, current_time, current_time))
        else:
            # Обновление времени последнего обращения
            await cursor.execute('''
                UPDATE users SET resent_time = ? WHERE user_id = ?
            ''', (current_time, user_id))
        await db.commit()

# Получение данных пользователя из базы данных
async def get_user(user_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.cursor()
        user_data = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return await user_data.fetchone()

# Обработка даты рождения, введенной пользователем
async def handle_birthdate(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    try:
        day, month = map(int, message.text.split('.'))
        if not (1 <= day <= 31 and 1 <= month <= 12):
            raise ValueError("Неправильная дата.")
        
        zodiac_sign = functions.get_zodiac_sign(day, month)
        birthdate = f"{day:02}.{month:02}"
        
        await add_user(user_id, full_name, username, birthdate, zodiac_sign)
        start_keyboard=create_forecast_keyboard() # Ошибка
        await message.answer(f"Вы <b>{zodiac_sign}</b>. Хотите узнать гороскоп на сегодня?", reply_markup=start_keyboard)
        
        await state.clear()

    except ValueError:
        await message.answer("Пожалуйста, введите дату в правильном формате (дд.мм).")
        print(f"User {user_id} entered an invalid date: {message.text}")

# Обработка команды /start
async def handle_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    # Проверка, есть ли пользователь в БД
    user_data = await get_user(user_id)
    
    if not user_data:
        # Спросим дату рождения, если пользователь не зарегистрирован
        await message.answer("Добро пожаловать! Пожалуйста, введите вашу дату рождения (дд.мм):")
        await state.set_state(AstroStates.waiting_for_birthdate)  
    else:
        start_keyboard=create_forecast_keyboard()
        await message.answer(f"Вы зарегистрированы как <b>{user_data['zodiac_sign']}</b>. Хотите узнать гороскоп на сегодня?", reply_markup=start_keyboard)
