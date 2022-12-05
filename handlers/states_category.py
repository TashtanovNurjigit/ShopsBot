from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import Message
from aiogram import Dispatcher
from data_base import sqlite3_db


class FSMAddCategory(StatesGroup):
    name = State()


async def add_category(message: Message):
    await FSMAddCategory.name.set()
    await message.reply('Напишите название категории', reply_markup=ReplyKeyboardRemove())


async def load_name_category(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await sqlite3_db.sql_add_commands(state, 'category')
    await message.reply('Новая категория добавлена в базу')
    await state.finish()


def register_states(dp: Dispatcher):
    dp.register_message_handler(add_category, commands=['add_category'], state=None)
    dp.register_message_handler(load_name_category, state=FSMAddCategory.name)
