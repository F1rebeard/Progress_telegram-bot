from re import split

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards import profile_kb


class AerobicData(StatesGroup):
    two_km_row = State()
    five_km_row = State()
    ten_km_row = State()
    row_step = State()
    row_mam = State()
    one_hour_row = State()
    ten_min_row = State()
    bike_step = State()
    bike_mam = State()
    ten_min_bike = State()
    skierg_step = State()
    skierg_mam = State()
    ten_min_skierg = State()


def transform_time_string(time: int) -> str:
    """
    Transforms time in sec, min or hours to a correct string format.
    If 8 seconds in will be 08 and etc.
    :param time:
    :return:
    """
    if time <= 9:
        return f'0{time}'
    return str(time)


def time_string_to_seconds(text: str) -> int or str:
    """
    Transforms string message from user like 12:22 where 12 - min and 22 - sec
    to total seconds
    :param text:
    :return:
    """
    min_and_seconds = split(':', text)
    if len(min_and_seconds) == 1:
        return int(min_and_seconds[0])
    if len(min_and_seconds) == 2:
        return int(min_and_seconds[0]) * 60 + int(min_and_seconds[1])
    elif len(min_and_seconds) == 3:
        return int(min_and_seconds[0]) * 3600 + int(min_and_seconds[1]) * 60\
            + int(min_and_seconds[2])


def seconds_to_time_string(total_seconds: int) -> str:
    """
    Transforms seconds to a readable message of time like 01:42:23.
    :param total_seconds:
    :return:
    """
    seconds = total_seconds % 60
    minutes = (total_seconds - seconds) // 60
    if minutes >= 60:
        left_minutes = minutes % 60
        hours = (minutes - left_minutes) // 60
        hours_str = transform_time_string(hours)
        minutes_str = transform_time_string(left_minutes)
        seconds_str = transform_time_string(seconds)
        return f"{hours_str}:{minutes_str}:{seconds_str}"
    return f"{transform_time_string(minutes)}:{transform_time_string(seconds)}"


async def two_km_row_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds a 2 km row time result into aerobic capacity table for user.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 360 <= converted_answer <= 900:
            async with state.proxy() as data:
                data['time_result'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 360:
            await message.answer('Флэш, ты ли это?')
        else:
            await message.answer('Введи согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи согласно формату!')


async def five_km_row_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
        Adds a 5 km row time result into aerobic capacity table for user.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 720 <= converted_answer <= 2400:
            async with state.proxy() as data:
                data['time_result'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 720:
            await message.answer('Флэш, ты ли это?')
        else:
            await message.answer('Введи согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи согласно формату!')


async def ten_km_row_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds a 10 km row time result into aerobic capacity table for user.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 1800 <= converted_answer <= 4200:
            async with state.proxy() as data:
                data['time_result'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 1800:
            await message.answer('Флэш, ты ли это?')
        else:
            await message.answer('Введи согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи согласно формату!')


async def row_step_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds rop step test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    watts = int(message.text)
    try:
        if 40 <= watts <= 600:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 600:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 40:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def row_mam_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds rop MAM-test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        watts = int(message.text)
        if 100 <= watts <= 1500:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 600:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 40:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def row_one_hour_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds rop MAM-test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    meters = int(message.text)
    try:
        if 3000 <= meters <= 18000:
            async with state.proxy() as data:
                data['time_result'] = meters
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif meters > 18000:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= meters < 3000:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def row_ten_minutes_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds 10 min row cal result to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    calories = int(message.text)
    try:
        if 50 <= calories <= 500:
            async with state.proxy() as data:
                data['time_result'] = calories
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif calories > 500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= calories < 50:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def bike_step_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds bike step test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    watts = int(message.text)
    try:
        if 40 <= watts <= 800:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 800:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 40:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def bike_mam_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds bike MAM-test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    watts = int(message.text)
    try:
        if 100 <= watts <= 2500:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 2500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 100:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def bike_ten_minutes_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds 10 min bike cal result to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        calories = int(message.text)
        if 25 <= calories <= 500:
            async with state.proxy() as data:
                data['time_result'] = calories
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif calories > 500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= calories < 25:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def skierg_step_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds skierg step test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        watts = int(message.text)
        if 40 <= watts <= 800:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 800:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 40:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def skierg_mam_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds skierg MAM-test max watt to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        watts = int(message.text)
        if 100 <= watts <= 1500:
            async with state.proxy() as data:
                data['time_result'] = watts
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif watts > 1500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= watts < 100:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')

async def skierg_ten_minutes_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds 10 min skierg cal result to table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        calories = int(message.text)
        if 50 <= calories <= 500:
            async with state.proxy() as data:
                data['time_result'] = calories
                data['date'] = datetime.now()
            await db.update_result_aerobic_movement(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.aerobic_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif calories > 500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= calories < 50:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


def register_aerobic_handelrs(dp: Dispatcher):
    dp.register_message_handler(two_km_row_result,
                                state=AerobicData.two_km_row)
    dp.register_message_handler(five_km_row_result,
                                state=AerobicData.five_km_row)
    dp.register_message_handler(ten_km_row_result,
                                state=AerobicData.ten_km_row)
    dp.register_message_handler(row_step_result,
                                state=AerobicData.row_step)
    dp.register_message_handler(row_mam_result,
                                state=AerobicData.row_mam)
    dp.register_message_handler(row_one_hour_result,
                                state=AerobicData.one_hour_row)
    dp.register_message_handler(row_ten_minutes_result,
                                state=AerobicData.ten_min_row)
    dp.register_message_handler(bike_step_result,
                                state=AerobicData.bike_step)
    dp.register_message_handler(bike_mam_result,
                                state=AerobicData.bike_mam)
    dp.register_message_handler(bike_ten_minutes_result,
                                state=AerobicData.ten_min_bike)
    dp.register_message_handler(skierg_step_result,
                                state=AerobicData.skierg_step)
    dp.register_message_handler(skierg_mam_result,
                                state=AerobicData.skierg_mam)
    dp.register_message_handler(skierg_ten_minutes_result,
                                state=AerobicData.ten_min_skierg)




