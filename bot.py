from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from secret import TOKEN
import sqlite3
from machine import *

bot = Bot(token=TOKEN)  # Тут подключаем самого бота
storage = MemoryStorage()  # Хранилище для машины состояний
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    with sqlite3.connect('ManMade.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT uid FROM local WHERE uid = ?", (message.from_user.id,))
        start = cursor.fetchall()
        start_inf = list(sum(start, ()))
        connect.commit()
        if start_inf == []:
            with sqlite3.connect('ManMade.db', timeout=60) as connect:
                cursor = connect.cursor()
                cursor.execute("INSERT INTO local (uid) VALUES (?)",
                               (message.from_user.id,))
                await message.answer(
                    f'🤖 {message.chat.first_name}, Добрый день, это бот для клиентов и владельцев компьютеров от компании MAN-MADE. 🤖\n')
                button_phone = types.KeyboardButton(text="Share", request_contact=True)
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                keyboard.add(button_phone)
                await message.answer(text='Для запуска бота необходимо предоставить свой номер телефона',
                                     reply_markup=keyboard)

                @dp.message_handler(content_types=["contact"])
                async def phone(message: types.Message):
                    if message.contact is not None:
                        phone_number = message.contact.phone_number
                        with sqlite3.connect('ManMade.db', timeout=60) as connect:
                            cursor = connect.cursor()
                            cursor.execute("UPDATE local set phone = ? WHERE uid = ?",(message.contact.phone_number, message.from_user.id,))
                            cursor.execute("SELECT phone FROM customers WHERE phone = ?", (phone_number,))

                            check_phone = cursor.fetchall()
                            phone_inf = list(sum(check_phone, ()))
                            connect.commit()
                            if phone_inf == []:
                                await message.answer(
                                    "К номеру телефона не привязан пользователь.\nДля уточнения подробностей позвоните по номеру 8-800-707-52-62")
                            else:
                                keyboard_main = InlineKeyboardMarkup(resize_keyboard=True, row_width=3).add(
                                    InlineKeyboardButton(text='Upgrade', callback_data="upg"),
                                    InlineKeyboardButton(text='Обслужить мой компьютер', callback_data="pc"),
                                    InlineKeyboardButton(text='Конфигурация моего компьютера', callback_data="conf"),
                                    InlineKeyboardButton(text='Написать в техподдержку', callback_data="teh"))
                                await message.answer(
                                    f"{message.chat.first_name}, рады приветствовать вас в нашем телеграм-боте. Здесь вы можете записаться на ряд наших услуг: UPGRADE и обслуживание. А также посмореть актуальную сборку вашего компьютера, Помимо этого бот будет присылать акции от нашей компании и персональные предложения для вас.",
                                    reply_markup=keyboard_main)

        else:
            keyboard_main = InlineKeyboardMarkup(resize_keyboard=True, row_width=3).add(
                InlineKeyboardButton(text='Upgrade', callback_data="upg"),
                InlineKeyboardButton(text='Обслужить мой компьютер', callback_data="pc"),
                InlineKeyboardButton(text='Конфигурация моего компьютера', callback_data="conf"),
                InlineKeyboardButton(text='Написать в техподдержку', callback_data="teh"))
            await message.answer(
                f"{message.chat.first_name}, рады приветствовать вас в нашем телеграм-боте. Здесь вы можете записаться на ряд наших услуг: UPGRADE и обслуживание. А также посмореть актуальную сборку вашего компьютера, Помимо этого бот будет присылать акции от нашей компании и персональные предложения для вас.",
                reply_markup=keyboard_main)

@dp.callback_query_handler(text="teh")
async def teh(callback: types.CallbackQuery):
    await callback.message.answer("Обратитесь к специалисту\nhttps://t.me/MAPC_TbI_XOPOLLI")

@dp.callback_query_handler(text="upg")
async def upg(callback: types.CallbackQuery):
    await callback.message.answer()

@dp.callback_query_handler(text="pc")
async def pc(callback: types.CallbackQuery):
    await callback.message.answer()

@dp.callback_query_handler(text="conf")
async def conf(callback: types.CallbackQuery):
    with sqlite3.connect('ManMade.db', timeout=60) as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM PC WHERE uid = ?",)
        await callback.message.answer()
