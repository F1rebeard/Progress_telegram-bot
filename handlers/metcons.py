from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards import profile_kb
from handlers.aerobic_capacity import time_string_to_seconds


class MetconsData(StatesGroup):
    hundred_burpees = State()
    karen = State()
    murph = State()
    cindy = State()
    linda = State()
    open_13_1 = State()
    kalsu = State()
    open_19_1 = State()
    open_16_5 = State()


async def one_hundred_burpees_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds a 150 burpees time result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 240 <= converted_answer <= 1800:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 240:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif converted_answer > 1800:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')

async def karen_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds Karen result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 180 <= converted_answer <= 1200:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 180:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif converted_answer > 1200:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


async def murph_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 1200 <= converted_answer <= 10800:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 1200:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif converted_answer > 10800:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


async def cindy_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 30 <= reps <= 1350:
            async with state.proxy() as data:
                data['time_result'] = reps
                data['date'] = datetime.now()
            await db.update_metcon_result(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 1350:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= reps < 50:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')

async def linda_reuslt(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 480 <= converted_answer <= 3600:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 480:
            await message.answer('Ты точно не ошибся? В стойку или в сед, а?'
                                 ' Честно говори!')
        elif converted_answer > 3600:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


async def open_13_1_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message: max watts from test
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 45 <= reps <= 500:
            async with state.proxy() as data:
                data['time_result'] = reps
                data['date'] = datetime.now()
            await db.update_metcon_result(state)
            await message.answer(
                'Данные обновлены!',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 500:
            await message.answer('Что-то невероятное! Не верю!')
        elif 0 <= reps < 45:
            await message.answer('Да ладно тебе скромничать')
        else:
            await message.answer('Положительное целое число!')
    except ValueError or TypeError:
        await message.answer('Положительное целое число!')


async def kalsu_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 600 <= converted_answer <= 5400:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 600:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif converted_answer > 5400:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


async def open_19_1_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 38 <= reps <= 400:
            async with state.proxy() as data:
                data['result_reps'] = reps
                data['date'] = datetime.now()
            await db.update_metcon_result(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 400:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif reps < 38:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


async def open_16_5_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds murph result to metcons table.
    :param message:
    :param state:
    :return:
    """
    try:
        converted_answer = time_string_to_seconds(message.text)
        if 360 <= converted_answer <= 1200:
            async with state.proxy() as data:
                data['result_time'] = converted_answer
                data['date'] = datetime.now()
            await db.update_time_result_metcon(state)
            await message.answer(
                'Данные обновлены',
                reply_markup=await profile_kb.metcon_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif converted_answer < 360:
            await message.answer('Ты точно не ошибся? Too fast!'
                                 ' Честно говори!')
        elif converted_answer > 1200:
            await message.answer('Там был чай с пироженкой между делом?')
        else:
            await message.answer('Введи время согласно формату!')
    except ValueError or TypeError:
        await message.answer('Введи время согласно формату!')


def register_metcon_handlers(dp: Dispatcher):
    dp.register_message_handler(one_hundred_burpees_result,
                                state=MetconsData.hundred_burpees)
    dp.register_message_handler(karen_result,
                                state=MetconsData.karen)
    dp.register_message_handler(murph_result,
                                state=MetconsData.murph)
    dp.register_message_handler(cindy_result,
                                state=MetconsData.cindy)
    dp.register_message_handler(linda_reuslt,
                                state=MetconsData.linda)
    dp.register_message_handler(open_13_1_result,
                                state=MetconsData.open_13_1)
    dp.register_message_handler(kalsu_result,
                                state=MetconsData.kalsu)
    dp.register_message_handler(open_19_1_result,
                                state=MetconsData.open_19_1)
    dp.register_message_handler(open_16_5_result,
                                state=MetconsData.open_16_5)




