from aiogram.dispatcher.filters.state import StatesGroup, State


class Driver_States(StatesGroup):
    full_name = State()
    birth_date = State()
    passport_one = State()
    passport_two = State()
    phone_number = State()
    driver_photo = State()
    car_photo = State()
    car_number = State()
    driver_check = State()
