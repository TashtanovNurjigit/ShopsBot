from config import dp
from aiogram import executor
from handlers import (
    client, states_products, states_category
)
from data_base import sqlite3_db


async def on_startup(_):
    sqlite3_db.sql_start()
    print('TeleBot')

client.register_client_handlers(dp)
states_products.register_states(dp)
states_category.register_states(dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
