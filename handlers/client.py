from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import bot
from keyboards.client_kb import kb_client
from data_base import sqlite3_db


# Отвечаем на команды "start", "help"
async def start(message: types.Message):
    await message.answer('Выберите действие', reply_markup=kb_client)


# Отвечаем на кнопку "Адрес"
async def address(message: types.Message):
    await message.answer('ул.Логвиненко 55')


# Выдаем список техник
async def get_products(message: types.Message):
    await sqlite3_db.sql_read_products(message)


async def get_category(message: types.Message):
    for obj in sqlite3_db.cursor.execute('SELECT name FROM category').fetchall():
        await bot.send_message(message.from_user.id, text=f'{obj[0]}\n', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Delete', callback_data=f'delete_{obj[0]}')))


async def delete(call: types.CallbackQuery):
    await sqlite3_db.delete(call.data.replace('delete_ ', ''))
    await call.answer(text=f'{call.data.replace("delete_ ", "")} удалена ', show_alert=True)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ok')


# Регистрируем все команды
def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(address, lambda message: message.text == 'Адрес магазина')
    dp.register_message_handler(get_products, commands=['get_products'])
    dp.register_message_handler(get_category, commands=['get_category'])
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_callback_query_handler(delete, lambda x: x.data and x.data.startswith('delete_'))
