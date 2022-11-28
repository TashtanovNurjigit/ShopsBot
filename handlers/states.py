from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message
from aiogram import Dispatcher
from data_base import sqlite3_db

class FSMAddItem(StatesGroup):
    name = State()
    photo = State()
    price = State()
    category = State()


# Запускаем машинное состояние
async def add_item(message: Message):
    await FSMAddItem.name.set()
    await message.reply('Напишите название товара', reply_markup=ReplyKeyboardRemove())


# Сохраняем название товара
async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAddItem.next()
    await message.reply('Отправьте фото товара')


# Сохраняем фото товара
async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAddItem.next()
    await message.reply('Напишите цену товара')


# Сохраняем цену товара
async def load_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await FSMAddItem.next()
    await message.reply('В какую категорию вводить товар')


# Сохраняем категорию товара
async def load_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    if message.text.lower() == 'бытовая техника':
        await sqlite3_db.sql_add_appliances(state)
        await message.reply('Ваш товар успешно сохранено в базе')
    elif message.text.lower() == 'телефоны':
        await sqlite3_db.sql_add_phones(state)
        await message.reply('Ваш товар успешно сохранено в базе')
    elif message.text.lower() == 'гаджеты':
        await sqlite3_db.sql_add_gadgets(state)
        await message.reply('Ваш товар успешно сохранено в базе')
    else:
        await message.reply('Такой категории нет в базе')

    await state.finish()


# Регистрируем все команды
def register_states(dp: Dispatcher):
    dp.register_message_handler(add_item, commands=['add_item'], state=None)
    dp.register_message_handler(load_name, state=FSMAddItem.name)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAddItem.photo)
    dp.register_message_handler(load_price, state=FSMAddItem.price)
    dp.register_message_handler(load_category, state=FSMAddItem.category)
