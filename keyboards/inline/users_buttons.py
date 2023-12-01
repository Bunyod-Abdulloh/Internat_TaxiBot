from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

internat_location_button = InlineKeyboardMarkup(row_width=1)
internat_location_button.add(InlineKeyboardButton(
    text="4 - internat",
    callback_data="internat_location")
)
