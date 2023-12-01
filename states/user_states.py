from aiogram.dispatcher.filters.state import StatesGroup, State


class PupilStates(StatesGroup):
    class_number = State()
    full_name = State()
    birth_date = State()
    pupil_photo = State()
    phone_number_of_parents = State()
    phone_number_of_teacher = State()
    get_home_location = State()
    get_work_location = State()
    get_other_location = State()
