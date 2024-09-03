import sys
import os
from datetime import datetime

from config import config

### handlers
import user
import keyboard_callback

import asyncio
import aiosqlite
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import html


# Определяем состояния
class AstroStates(StatesGroup):
    waiting_for_birthdate = State()

async def main():
    # Создание экземпляра диспетчера
    storage = MemoryStorage()  # Хранилище состояний в памяти
    bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    
    # Инициализация БД
    await user.initialize_db()
    
    dp.message.register(user.handle_start, Command("start"))
    dp.message.register(user.handle_birthdate, StateFilter(AstroStates.waiting_for_birthdate))    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

