from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
from states.admin_states import AdminStates


@dp.callback_query_handler(text_contains='admincheckdriver_', state=AdminStates.page_one)
async def adm_check_driver(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split('_')[1])
    data = await state.get_data()
    dr_full_name = data['driver_fullname']
    dr_birth_date = data['driver_birth_date']
    dr_phone_number = data['driver_phone']
    dr_passport_one = data['driver_passport_one']
    dr_passport_two = data['driver_passport_two']
    dr_photo = data['driver_photo']
    car_photo = data['car_photo']
    car_number = data['car_number']

    await db.add_drivers(full_name=dr_full_name,
                         birth_date=dr_birth_date,
                         phone_number=dr_phone_number,
                         passport_one=dr_passport_one,
                         passport_two=dr_passport_two,
                         driver_photo=dr_photo,
                         car_photo=car_photo,
                         car_number=car_number,
                         telegram_id=user_id)

    await state.finish()


@dp.callback_query_handler(text_contains='admincanceldriver_', state=AdminStates.page_one)
async def adm_cancel_driver(call: types.CallbackQuery, state: FSMContext):
    # print(call.data)
    user_id = call.data.split('_')[1]
    print(user_id)
