from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message
from aiogram import Dispatcher
from data_base import sqlite3_db


class FSMAddProducts(StatesGroup):
    name = State()
    photo = State()
    price = State()
    category = State()


# Запускаем машинное состояние
async def add_products(message: Message):
    await FSMAddProducts.name.set()
    await message.reply('Напишите название товара', reply_markup=ReplyKeyboardRemove())


# Сохраняем название товара
async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAddProducts.next()
    await message.reply('Отправьте фото товара')


# Сохраняем фото товара
async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAddProducts.next()
    await message.reply('Напишите цену товара')


# Сохраняем цену товара
async def load_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAddProducts.next()
    await message.answer(f'Выберите категорию товара:\n')
    await sqlite3_db.sql_read_category(message)


# Сохраняем категорию товара и записываем в базе данных
async def load_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await sqlite3_db.sql_add_commands(state, 'products')
    await message.reply('Ваш товар успешно сохранено в базе')
    await state.finish()


# Регистрируем все команды
def register_states(dp: Dispatcher):
    dp.register_message_handler(add_products, commands=['add_products'], state=None)
    dp.register_message_handler(load_name, state=FSMAddProducts.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAddProducts.photo)
    dp.register_message_handler(load_price, state=FSMAddProducts.price)
    dp.register_message_handler(load_category, state=FSMAddProducts.category)
