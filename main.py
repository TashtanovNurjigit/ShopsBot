from config import dp
from aiogram import executor
from handlers import client, states
from data_base import sqlite3_db


async def on_startup(_):
    sqlite3_db.sql_start()
    print('TeleBot')

client.register_client_handlers(dp)
states.register_states(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
