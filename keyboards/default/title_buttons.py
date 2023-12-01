from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

title_buttons = ReplyKeyboardMarkup(resize_keyboard=True)
title_buttons.row('🏫 Maktabdan olish', '🏘 Maktabga yuborish')
title_buttons.row('👮‍♂️ Adminga murojaat')

title_back_button = ReplyKeyboardMarkup(resize_keyboard=True)
title_back_button.row('🔙 Ortga')

