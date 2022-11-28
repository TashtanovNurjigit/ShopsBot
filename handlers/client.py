from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove

from keyboards.client_kb import kb_client
from data_base import sqlite3_db


# Отвечаем на команды "start", "help"
async def start(message: types.Message):
    await message.answer('Выберите действие', reply_markup=kb_client)


# Отвечаем на кнопку "Адрес"
async def address(message: types.Message):
    await message.answer('ул.Логвиненко 55')


# Отвечаем на кнопку "Список категорий"
async def category_list(message: types.Message):
    await message.answer('1.Бытовая техника “/appliances”\n'
                         '2. Телефоны “/phones”\n'
                         '3.Гаджеты “/gadgets”', reply_markup=ReplyKeyboardRemove())


# Выдаем список техник по команде "appliances"
async def appliances(message: types.Message):
    await sqlite3_db.sql_read_appliances(message)


# Выдаем список телефонов по команде "phones"
async def phones(message: types.Message):
    await sqlite3_db.sql_read_phones(message)


# Выдаем список гаджетов по команде "gadgets"
async def gadgets(message: types.Message):
    await sqlite3_db.sql_add_gadgets(message)


# Регистрируем все команды
def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(address, lambda message: message.text == 'Адрес магазина')
    dp.register_message_handler(category_list, lambda message: message.text == 'Список категорий')
    dp.register_message_handler(appliances, commands=['appliances'])
    dp.register_message_handler(phones, commands=['phones'])
    dp.register_message_handler(gadgets, commands=['gadgets'])
