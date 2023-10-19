from aiogram import types, Dispatcher
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards.profile_kb import (categories_keyboard,
                                  biometrics_inline_btns,
                                  create_inline_keyboard)


class BiometricsData(StatesGroup):
    height = State()
    weight = State()
    birthdate = State()

async def height_updated(message: types.Message,
                         state: FSMContext) -> None:
    """
    Get text from user message with height state active, if text is correct
    finish fsm and add weight to database for current user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 150 < int(message.text) <= 220:
            async with state.proxy() as data:
                data['height'] = int(message.text)
            await db.update_user_height(message.from_user.id, state)
            biometrics_inline_kb = create_inline_keyboard(
                await biometrics_inline_btns(message.from_user.id))
            await message.answer(f"Ваш рост обновлен - {data['height']} cм.",
                                 reply_markup=biometrics_inline_kb)
            await state.finish()
        elif 0 < int(message.text) < 150:
            await message.answer('Ты хоббит?')
        elif int(message.text) >= 220:
            await message.answer('Зачем тебе кроссфит? Есть баcкетбол!')
        else:
            await message.answer('Мир зазеркалья 💩?')
    except ValueError or TypeError:
        await message.answer('Эмм, это не число! 🤹')


async def weight_updated(message: types.Message,
                         state: FSMContext) -> None:
    """
    Get text from user message with weight state active, if text is correct
    finish fsm and add weight to database for current user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 < int(message.text) < 38:
            await message.answer('Ты точно кушаешь? 🍩')
        elif int(message.text) > 140:
            await message.answer('Хафтор Бьйорнсон, ты ли это!? 🥨')
        elif 38 <= int(message.text) <= 140:
            async with state.proxy() as data:
                data['weight'] = int(message.text)
            await db.update_user_weight(message.from_user.id, state)
            biometrics_inline_kb = create_inline_keyboard(
                await biometrics_inline_btns(message.from_user.id))
            await message.answer(f"Ваш вес обновлен - {data['weight']} кг.",
                                 reply_markup=biometrics_inline_kb)
            await state.finish()
        else:
            await message.answer('Не надо так 🤹')
    except ValueError or TypeError:
        await message.answer('Эмм, это не число! 🤹')


async def birthdate_update(message: types.Message, state: FSMContext) -> None:
    """
    Adds user birthdate to database.
    :param message:
    :param state:
    :return:
    """
    eighteen_years = timedelta(days=365) * 18
    sixty_years = timedelta(days=365) * 60
    very_young = datetime.now().date() - eighteen_years
    very_old = datetime.now().date() - sixty_years
    try:

        users_birthdate = datetime.strptime(message.text, '%d-%m-%Y').date()
        if very_old < users_birthdate < very_young:
            async with state.proxy() as data:
                data['birthdate'] = users_birthdate
            await db.update_user_birthdate(message.from_user.id, state)
            biometrics_inline_kb = create_inline_keyboard(
                await biometrics_inline_btns(message.from_user.id))
            await message.answer(f'Обновлено! Твой день рождения -'
                                 f' {data["birthdate"]}',
                                 reply_markup=biometrics_inline_kb)
            await state.finish()
        else:
            await message.answer('Слишком young 👶 или cлишком old 🧙‍♂️')
    except ValueError:
        await message.answer('Напиши дату согласно формату: дд-мм-гггг')


def register_biometrics_handlers(dp: Dispatcher):
    dp.register_message_handler(height_updated,
                                state=BiometricsData.height)
    dp.register_message_handler(weight_updated,
                                state=BiometricsData.weight)
    dp.register_message_handler(birthdate_update,
                                state=BiometricsData.birthdate)

