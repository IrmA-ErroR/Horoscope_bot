from config import config
from . import functions

import asyncio
import aiosqlite
from datetime import datetime


from aiogram import types, F
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import html

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage


async def initialize_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                date_birth TEXT,
                zodiac_sign TEXT,
                first_time TEXT NOT NULL,
                resent_time TEXT NOT NULL        
            )
        ''')
        await db.commit()

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
        await message.answer(f"Вы <b>{zodiac_sign}</b>. Хотите узнать гороскоп на сегодня?")
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите дату в правильном формате (дд.мм).")


async def get_user(user_id):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cursor = await db.cursor()
        user_data = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return await user_data.fetchone()


async def handle_start(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    
    # Проверка, есть ли пользователь в БД
    user_data = await get_user(user_id)
    
    if not user_data:
        # Спросим дату рождения, если пользователь не зарегистрирован
        await message.answer("Добро пожаловать! Пожалуйста, введите вашу дату рождения (дд.мм):")
        await AstroStates.waiting_for_birthdate.set()
    else:
        await message.answer(f"Вы уже зарегистрированы как <b>{user_data['zodiac_sign']}<\b>. Хотите узнать гороскоп на сегодня?")