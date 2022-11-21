from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from secret import TOKEN
import logging

bot = Bot(token=TOKEN)  # Тут подключаем самого бота
storage = MemoryStorage()  # Хранилище для машины состояний
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

