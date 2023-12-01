from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def driver_check_buttons(user_id=None):
    markup = InlineKeyboardMarkup(row_width=2)

    if user_id:
        markup.insert(InlineKeyboardButton(text='✅ Tasdiqlash',
                                           callback_data=f'admincheckdriver_{user_id}'))
        markup.insert(InlineKeyboardButton(text='❎ Bekor qilish',
                                           callback_data=f'admincanceldriver_{user_id}'))
    elif user_id is None:
        markup.insert(InlineKeyboardButton(text='✅ Tasdiqlash',
                                           callback_data=f'driver_check'))
        markup.insert(InlineKeyboardButton(text='♻️Qayta kiritish',
                                           callback_data='driver_re_enter'))
    return markup


def driver_delete_button(driver_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text='❌ O\'chirish',
                                       callback_data=f'driverdelete_{driver_id}'))
    markup.insert(InlineKeyboardButton(text='🏡 Bosh menyu',
                                       callback_data='main_menu'))
    return markup
