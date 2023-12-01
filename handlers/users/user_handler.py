# import math
# from geopy.distance import geodesic as GD
# from aiogram import types
# from aiogram.dispatcher import FSMContext
#
# from keyboards.default.title_buttons import title_buttons
# from keyboards.default.users_custom_buttons import user_location_button
# from keyboards.inline.users_buttons import internat_location_button
# from loader import dp, bot, db
# from states.user_states import UserStates, PupilStates
# from data.locations import schools, my_locations
# from utils.misc.get_distance import calc_distance
#
#
# @dp.message_handler(text='🏫 Maktabdan olish', state='*')
# async def user_title(message: types.Message):
#
#     pupil = await db.select_pupil(
#         telegram_id=message.from_user.id
#     )
#
#     if pupil:
#         await message.answer(
#             text='Maktabni tanlang:',
#             reply_markup=internat_location_button)
#     else:
#         await message.answer('Siz avval ro\'yxatdan o\'tmagansiz! Keling avval farzandingiz haqidagi ma\'lumotlarni '
#                              'bizning ma\'lumotlar omborimizga kiritamiz. Farzandingiz sinfini kiriting:')
#         await PupilStates.class_number.set()
#
#
# @dp.callback_query_handler(text='internat_location', state='*')
# async def internat_location(call: types.CallbackQuery, state: FSMContext):
#     await call.message.answer(
#         text='Farzandingiz kelishi kerak bo\'lgan manzil lokatsiyasini yuboring:',
#         reply_markup=user_location_button
#     )
#     await UserStates.get_location.set()
#
#
# @dp.message_handler(state=UserStates.get_location, content_types=['location', 'text'])
# async def user_get_location(message: types.Message, state: FSMContext):
#     if message.content_type == 'text':
#         if message.text == '🔙 Ortga':
#             await message.answer(
#                 text='Ortga',
#                 reply_markup=title_buttons
#             )
#             await state.finish()
#
#     elif message.content_type == 'location':
#         print(message)
#         latitude = message.location.latitude
#         longitude = message.location.longitude

    # await message.answer_location(
    #     latitude=41.25918411129535,
    #     longitude=69.2008413718809
    # )


# 41.25918411129535, 69.2008413718809

# @dp.message_handler(state=UserStates.fio)
# async def user_fio(message: types.Message, state: FSMContext):
#     yandex mashina.tex pasporti, mashina rasmi, haydovchi pasporti va rasmi, haydovchi pasporti selfi qilingan rasmi.


# @dp.message_handler(text="salom", state='*')
# async def sample_func(message: types.Message, state: FSMContext):
#
#     await bot.send_location(
#         chat_id=message.from_user.id,
#         latitude=schools['Internat']['latitude'],
#         longitude=schools['Internat']['longitude'],
#         live_period=3600
#     )

# First, import the geodesic module from the geopy library

# Then, load the latitude and longitude data for New York & Texas
# Internat = (schools['Internat']['latitude'], schools['Internat']['longitude'])
# Home = (my_locations['Home']['latitude'], my_locations['Home']['longitude'])
#
# location = GD(Internat, Home).kilometers

import json

x = '{"status": "Yor yorni boplabsiz)"}'

print(type(x))

data = json.loads(x)

print(data)


