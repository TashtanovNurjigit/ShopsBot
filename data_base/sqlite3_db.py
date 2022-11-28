import sqlite3 as sq

from config import bot


# Запуск базы данных
def sql_start():
    global base, cursor
    base = sq.connect('Товары')
    cursor = base.cursor()
    if base:
        print('DB connected')
    base.execute('CREATE TABLE IF NOT EXISTS appliances(name TEXT, photo TEXT, price TEXT, category TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS phones(name TEXT, photo TEXT, price TEXT, category TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS gadgets(name TEXT, photo TEXT, price TEXT, category TEXT)')
    base.commit()


# Сохранение товаров в категорию Бытовая техника
async def sql_add_appliances(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO appliances VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Сохранение товаров в категорию Телефоны
async def sql_add_phones(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO phones VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Сохранение товаров в категорию Гаджеты
async def sql_add_gadgets(state):
    async with state.proxy() as data:
        cursor.execute('INSERT INTO gadgets VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# Чтение с таблицы Бытовая техника
async def sql_read_appliances(message):
    for ret in cursor.execute('SELECT * FROM appliances').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'{ret[0]}\n Цена: {ret[2]}\n Категория: {ret[-1]}')


# Чтение с таблицы телефоны
async def sql_read_phones(message):
    for ret in cursor.execute('SELECT * FROM phones').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'{ret[0]}\n Цена: {ret[2]}\n Категория: {ret[-1]}')


# Чтение с таблицы Гаджеты
async def sql_read_gadgets(message):
    for ret in cursor.execute('SELECT * FROM gadgets').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'{ret[0]}\n Цена: {ret[2]}\n Категория: {ret[-1]}')
