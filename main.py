import sys
import os

# Добавляем директорию проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from handlers import user
from config import config

import asyncio
from random import randint
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
import html

from handlers import user

# Определяем состояния
class AstroStates(StatesGroup):
    waiting_for_birthdate = State()

async def main():
    # Создание экземпляра диспетчера
    storage = MemoryStorage()  # Хранилище состояний в памяти
    bot = Bot(token=config.TOKEN,  default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot = Bot(token=config.TOKEN)
    dp = Dispatcher(storage=storage)
    
    # Инициализация БД
    await user.initialize_db()
    
    dp.message.register(user.handle_start, Command("start"))
    dp.message.register(user.handle_birthdate, state=AstroStates.waiting_for_birthdate)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

