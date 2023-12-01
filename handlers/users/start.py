from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.title_buttons import title_buttons
from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!"
                         f"\n\n<b>Internat_taxi</b> botimizga xush kelibsiz!"
                         f"\n\nBiz Sizga farzandlaringizni maktab yoki biror o'quv dargohlariga olib borib qo'yish va "
                         f"olib kelish hizmatlarini taklif qilamiz!"
                         f"\n\nMarhamat, tugmalardan birini tanlang:",
                         reply_markup=title_buttons)
    await state.finish()
