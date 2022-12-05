import sqlite3 as sq

from config import bot


# Запуск базы данных
def sql_start():
    global base, cursor
    base = sq.connect('Products')
    cursor = base.cursor()
    if base:
        print('DB connected')
        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS category(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
            '''
        )
        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                photo TEXT,
                price TEXT,
                category TEXT,
                FOREIGN KEY(category) REFERENCES category(name)
            )
            '''
        )
        base.commit()


async def sql_add_commands(state, table):
    query = None
    if table == 'products':
        query = f'INSERT INTO {table} VALUES(?, ?, ?, ?, ?)'
    elif table == 'category':
        query = f'INSERT INTO {table} VALUES(?, ?)'
    async with state.proxy() as data:
        cursor.execute(query, (None, *tuple(data.values())))
        base.commit()


async def sql_read_products(message):
    query = f'SELECT * FROM products '
    for ret in cursor.execute(query).fetchall():
        await bot.send_photo(message.from_user.id, ret[2], f'{ret[1]}\n Цена: {ret[3]}\n Категория: {ret[-1]}')


async def sql_read_category(message):
    mes = ''
    for obj in cursor.execute('SELECT name FROM category').fetchall():
        mes += f'{obj[0]}\n'
    await message.answer(mes)


async def delete(data):
    cursor.execute('DELETE FROM category WHERE name = ?', (data,))
    base.commit()
