from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_location_button = ReplyKeyboardMarkup(resize_keyboard=True)
user_location_button.add(KeyboardButton(
    text='📍 Lokatsiya yuborish', request_location=True
))
user_location_button.add(KeyboardButton(
    text='🔙 Ortga'
))
