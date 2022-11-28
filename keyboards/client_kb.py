from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('Адрес магазина')
b2 = KeyboardButton('Список категорий')
b3 = KeyboardButton('/add_item')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).insert(b2)
kb_client.add(b3)

