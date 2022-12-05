from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('Адрес магазина')
b2 = KeyboardButton('/get_products')
b3 = KeyboardButton('/add_products')
b4 = KeyboardButton('/add_category')
b5 = KeyboardButton('/get_category')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).insert(b2)
kb_client.add(b3).insert(b4).insert(b5)

