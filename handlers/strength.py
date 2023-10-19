from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards.profile_kb import strength_inline_keyboard


class StrengthData(StatesGroup):
    movement = State()
    date = State()
    front_squat = State()
    back_squat = State()
    overhead_squat = State()
    bench_press = State()
    push_press = State()
    deadlift = State()
    clean_lift = State()
    snatch_lift = State()


async def front_squat_result(message: types.Message,
                             state: FSMContext) -> None:
    """
    Adds front squat result to strength table with today date and telegram id
    of user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 220:
            async with state.proxy() as data:
                data['front_squat'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 220:
            await message.answer('Тут без видео никак, или парочки домкратов!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')


async def back_squat_result(message: types.Message,
                            state: FSMContext) -> None:
    """
    Add back squat result to strength table with today date and telegram id
    of user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 250:
            async with state.proxy() as data:
                data['back_squat'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 250:
            await message.answer('Тут без видео никак, или парочки домкратов!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')
        

async def bench_press_result(message: types.Message,
                             state: FSMContext) -> None:
    """
    Add bench press result to strength table with today date and telegram id
    of user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 180:
            async with state.proxy() as data:
                data['bench_press'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 180:
            await message.answer('Тут без видео никак, или парочки домкратов!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')
        

async def overhead_squat_result(message: types.Message,
                                state: FSMContext) -> None:
    """
    Add overhead squat result to strength table with today date and telegram id
    of user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 180:
            async with state.proxy() as data:
                data['overhead_squat'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 180:
            await message.answer('Тут без видео никак, или парочки домкратов!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')
        

async def push_press_result(message: types.Message,
                            state: FSMContext) -> None:
    """
    Add push press result to strength table with today date and telegram id
    of user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 150:
            async with state.proxy() as data:
                data['push_press'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 150:
            await message.answer('Тут без видео никак, или парочки домкратов!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')


async def deadlift_result(message: types.Message, state: FSMContext) -> None:
    """
    Add deadlift result to strength table.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 300:
            async with state.proxy() as data:
                data['deadlift'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 300:
            await message.answer('Уже Стронгмэн пошёл какой-то!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def clean_lift_result(message: types.Message, state: FSMContext) -> None:
    """
    Add clean lift result to strength table for user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 300:
            async with state.proxy() as data:
                data['clean_lift'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 300:
            await message.answer('Уже олимпийские игры по ТА!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def snatch_lift_result(message: types.Message, state: FSMContext) -> None:
    """
    Add snatch lift result to strength table for user.
    :param message:
    :param state:
    :return:
    """
    try:
        if 0 <= float(message.text) <= 300:
            async with state.proxy() as data:
                data['snatch_lift'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_strength_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await strength_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 300:
            await message.answer('Уже олимпийские игры по ТА!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


def register_strength_handlers(dp: Dispatcher):
    dp.register_message_handler(front_squat_result,
                                state=StrengthData.front_squat)
    dp.register_message_handler(back_squat_result,
                                state=StrengthData.back_squat)
    dp.register_message_handler(overhead_squat_result,
                                state=StrengthData.overhead_squat)
    dp.register_message_handler(bench_press_result,
                                state=StrengthData.bench_press)
    dp.register_message_handler(push_press_result,
                                state=StrengthData.push_press)
    dp.register_message_handler(deadlift_result,
                                state=StrengthData.deadlift)
    dp.register_message_handler(clean_lift_result,
                                state=StrengthData.clean_lift)
    dp.register_message_handler(snatch_lift_result,
                                state=StrengthData.snatch_lift)
