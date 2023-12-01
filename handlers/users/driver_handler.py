from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.title_buttons import title_back_button, title_buttons
from keyboards.inline.driver_inline_buttons import driver_check_buttons, driver_delete_button
from loader import dp, bot, db
from states.admin_states import AdminStates
from states.driver_states import Driver_States


# @dp.message_handler(content_types=['photo'], state='*')
# async def rasm_id(message: types.Message, state: FSMContext):
# await message.answer(text=f'<code>{message.photo[-1].file_id}</code>')

@dp.message_handler(commands=['drivers'], state='*')
async def driver_title(message: types.Message):
    driver = await db.select_driver(telegram_id=message.from_user.id)
    if driver:
        dr_full_name = driver[1]
        dr_birth_date = driver[2]
        dr_phone_number = driver[3]
        dr_passport_one = driver[4]
        dr_passport_two = driver[5]
        dr_photo = driver[6]
        car_photo = driver[7]
        car_number = driver[8]

        album = types.MediaGroup()
        album.attach_photo(photo=dr_photo)
        album.attach_photo(photo=dr_passport_one)
        album.attach_photo(photo=dr_passport_two)
        album.attach_photo(photo=car_photo,
                           caption=f'<i>Haydovchi ism sharifi: <b>{dr_full_name}</b></i>'
                                   f'\n\n<i>Tug\'ilgan sana: <b>{dr_birth_date}</b></i>'
                                   f'\n\n<i>Telefon raqam: <b>{dr_phone_number}</b></i>'
                                   f'\n\n<i>Mashina raqami: <b>{car_number}</b></i>'
                           )
        await message.answer_media_group(
            media=album
        )
        await message.answer(
            text='<i>Ma\'lumotlaringizni o\'chirishni xohlasangiz <b>O\'chirish</b> tugmasini bosing!</i>',
            reply_markup=driver_delete_button(
                driver_id=message.from_user.id
            )
        )
    else:
        await message.answer(
            text='Ism, familiya va otangizni ismini kiriting:'
        )
        await Driver_States.full_name.set()


@dp.callback_query_handler(text_contains='driverdelete_', state='*')
async def driver_delete_keys(call: types.CallbackQuery):
    driver_id = int(call.data.split('_')[1])
    await db.delete_drivers(
        telegram_id=driver_id
    )
    await call.answer(
        text='Ma\'lumotlaringiz o\'chirildi!',
        show_alert=True
    )
    await call.message.delete()


@dp.callback_query_handler(text='main_menu', state='*')
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    await call.message.answer(
        text='Bosh menyu',
        reply_markup=title_buttons
    )
    await state.finish()


@dp.message_handler(state=Driver_States.full_name)
async def driver_fio(message: types.Message, state: FSMContext):
    await state.update_data(driver_full_name=message.text)
    await message.answer(text='Tug\'ilgan kun, oy, yilingizni kiriting: '
                              '\n\n<b>(Misol: 05.05.1900)</b>',
                         reply_markup=title_back_button)

    await Driver_States.birth_date.set()


@dp.message_handler(state=Driver_States.birth_date)
async def driver_birth_date(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer(text='Ism, familiya va otangizni ismini kiriting:')
        await Driver_States.full_name.set()
    else:
        await state.update_data(driver_birth_date=message.text)
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINFWTrN3DA0qYmxo0T5-fAQSz7o74aAAJezzEbcItYS6cQvOcZk0ArAQADAgADeQADMAQ',
            caption='Pasportingiz rasmini yuboring:')
        await Driver_States.passport_one.set()


# haydovchilik guvohnomasini rasmini olish yandex kamida 17 foiz oladi

@dp.message_handler(state=Driver_States.passport_one, content_types=['photo', 'text'])
async def driver_passport(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer(text='Tug\'ilgan kun, oy, yilingizni kiriting: '
                                  '\n\n<b>(Misol: 05.05.1900)</b>')
        await Driver_States.birth_date.set()

    else:
        await state.update_data(driver_passport_one=message.photo[-1].file_id)
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINF2TrN50oS8jOSIiGMDKXsJ-FowJkAAJgzzEbcItYSydq53z_wxpVAQADAgADeAADMAQ',
            caption='Ro\'yxatga qo\'yilgan joy rasmini yuboring:')
        await Driver_States.passport_two.set()


@dp.message_handler(state=Driver_States.passport_two, content_types=['photo', 'text'])
async def driver_passport_two(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINFWTrN3DA0qYmxo0T5-fAQSz7o74aAAJezzEbcItYS6cQvOcZk0ArAQADAgADeQADMAQ',
            caption='Pasportingiz rasmini yuboring:')
        await Driver_States.passport_one.set()

    else:
        await state.update_data(driver_passport_two=message.photo[-1].file_id)
        await message.answer(text='Telefon raqamingingizni kiriting:'
                                  '\n\n<b>+9989********</b>')
        await Driver_States.phone_number.set()


@dp.message_handler(state=Driver_States.phone_number)
async def driver_phone_number(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINF2TrN50oS8jOSIiGMDKXsJ-FowJkAAJgzzEbcItYSydq53z_wxpVAQADAgADeAADMAQ',
            caption='Ro\'yxatga qo\'yilgan joy rasmini yuboring:')
        await Driver_States.passport_two.set()

    else:
        await state.update_data(driver_phone=message.text)
        await message.answer(text='O\'z rasmingizni yuboring:')
        await Driver_States.driver_photo.set()


@dp.message_handler(state=Driver_States.driver_photo, content_types=['photo', 'text'])
async def driver_photo(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer(text='Telefon raqamingingizni kiriting:'
                                  '\n\n<b>+9989********</b>')
        await Driver_States.phone_number.set()

    else:
        await state.update_data(driver_photo=message.photo[-1].file_id)
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINHGTrPAXMIXCn3N9tevRoWymhPZ-WAAKEzzEbcItYS7T955u7ugtHAQADAgADbQADMAQ',
            caption='Mashinangiz rasmini yuboring:'
                    '\n\n(rasm mashina old tomonidan, raqamlari ham ko\'ringan holatda bo\'lishi lozim!)')
        await Driver_States.car_photo.set()


@dp.message_handler(state=Driver_States.car_photo, content_types=['photo', 'text'])
async def driver_car_photo(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer(text='O\'z rasmingizni yuboring:')
        await Driver_States.driver_photo.set()

    else:
        await state.update_data(car_photo=message.photo[-1].file_id)
        await message.answer(text='Mashinangiz raqamini kiriting:'
                                  '<b>\n\n(Misol: 01 W 007 TN)</b>')
        await Driver_States.car_number.set()


@dp.message_handler(state=Driver_States.car_number)
async def driver_car_number(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga':
        await message.answer_photo(
            photo='AgACAgIAAxkBAAINHGTrPAXMIXCn3N9tevRoWymhPZ-WAAKEzzEbcItYS7T955u7ugtHAQADAgADbQADMAQ',
            caption='Mashinangiz rasmini yuboring:'
                    '\n\n(rasm mashina old tomonidan, raqamlari ham ko\'ringan holatda bo\'lishi lozim!)')
        await Driver_States.car_photo.set()

    else:

        await state.update_data(car_number=message.text)

        data = await state.get_data()

        album = types.MediaGroup()
        album.attach_photo(photo=data['driver_passport_one'])
        album.attach_photo(photo=data['driver_passport_two'])
        album.attach_photo(photo=data['driver_photo'])
        album.attach_photo(photo=data['car_photo'],
                           caption=f"<i>Haydovchi ism sharifi: <b>{data['driver_full_name']}</b></i>"
                                   f"<i>\n\nTug'ilgan sana: <b>{data['driver_birth_date']}</b></i>"
                                   f"<i>\n\nTelefon raqami: <b>{data['driver_phone']}</b></i>"
                                   f"<i>\n\nMashina raqami: <b>{message.text}</b></i>")

        await message.answer_media_group(media=album)
        await message.answer(text='Yuqoridagi ma\'lumotlarni tasdiqlaysizmi?',
                             reply_markup=driver_check_buttons())
        await Driver_States.driver_check.set()


@dp.message_handler(state=Driver_States.driver_check)
async def driver_check_function(message: types.Message):
    if message.text == '🔙 Ortga':
        await message.answer(text='Mashinangiz raqamini kiriting:'
                                  '<b>\n\n(Misol: 01 W 007 TN)</b>')
        await Driver_States.car_number.set()


@dp.callback_query_handler(state=Driver_States.driver_check)
async def driver_check_function(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    dr_full_name = data['driver_full_name']
    dr_birth_date = data['driver_birth_date']
    dr_phone = data['driver_phone']
    dr_passport_one = data['driver_passport_one']
    dr_passport_two = data['driver_passport_two']
    dr_photo = data['driver_photo']
    car_photo = data['car_photo']
    car_number = data['car_number']

    dr_id = call.from_user.id

    album = types.MediaGroup()

    if call.data == 'driver_check':
        await call.message.answer(text='Ma\'lumotlar uchun tashakkur! Admin ma\'lumotlaringizni tasdiqlagach, '
                                       'buyurtmalar qabul qilishni boshlashingiz mumkin!')
        album.attach_photo(photo=dr_passport_one)
        album.attach_photo(photo=dr_passport_two)
        album.attach_photo(photo=dr_photo)
        album.attach_photo(photo=car_photo,
                           caption=f"Botga yangi haydovchining ma'lumotlari qabul qilindi!"
                                   f"\n\n<i>Haydovchi ism sharifi: <b>{dr_full_name}</b></i>"
                                   f"<i>\n\nTug'ilgan sana: <b>{dr_birth_date}</b></i>"
                                   f"<i>\n\nTelefon raqami: <b>{dr_phone}</b></i>"
                                   f"<i>\n\nMashina raqami: <b>{car_number}</b></i>")
        await bot.send_media_group(chat_id=ADMINS[0], media=album)
        await bot.send_message(chat_id=ADMINS[0],
                               text=f'Tasdiqlaysizmi?',
                               reply_markup=driver_check_buttons(user_id=dr_id))
        await AdminStates.page_one.set()

    elif call.data == 'driver_re_enter':
        await call.message.answer(text='Ma\'lumotlaringizni qayta kiritishingiz mumkin!'
                                       '\n\nIsm, familiya va otangizni ismini kiriting:')
        await Driver_States.full_name.set()
