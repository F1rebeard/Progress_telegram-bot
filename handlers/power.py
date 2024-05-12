from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards.profile_kb import power_inline_keyboard


class PowerData(StatesGroup):
    movement = State()
    data = State()
    long_jump = State()
    snatch = State()
    power_snatch = State()
    hang_snatch = State()
    hang_power_snatch = State()
    clean = State()
    power_clean = State()
    power_jerk = State()
    jerk = State()
    split_jerk = State()
    thruster = State()
    cluster = State()


async def long_jump_result(message: types.Message, state: FSMContext) -> None:
    """
    Adds long jump result to power table with today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 50 <= float(message.text) <= 400:
            async with state.proxy() as data:
                data['long_jump'] = float(message.text)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 400:
            await message.answer('Кенгуру?')
        elif float(message.text) < 50:
            await message.answer('Можно просто длину шага, хотя бы 🤪')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')


async def snatch_result(message: types.Message, state: FSMContext) -> None:
    """
    Adds snatch result to power table with today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 175:
            async with state.proxy() as data:
                data['snatch'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 175:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def power_snatch_result(message: types.Message,
                              state: FSMContext) -> None:
    """
    Adds power snatch result to power table today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 175:
            async with state.proxy() as data:
                data['power_snatch'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 175:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def hang_snatch_result(message: types.Message,
                             state: FSMContext) -> None:
    """
    Adds hang snatch result to power table today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['hang_snatch'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 200:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def hang_power_snatch_result(message: types.Message,
                                   state: FSMContext) -> None:
    """
    Adds hang power snatch result to power
    table today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['hang_power_snatch'] = round(
                    float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 200:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def clean_result(message: types.Message,
                       state: FSMContext) -> None:
    """
    Adds clean result to power
    table today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 250:
            async with state.proxy() as data:
                data['clean'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 250:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def power_clean_result(message: types.Message,
                             state: FSMContext) -> None:
    """
    Adds power clean result to power table today date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['power_clean'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 200:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def power_jerk_result(message: types.Message,
                            state: FSMContext) -> None:
    """
    Adds power jerk result to power table date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['power_jerk'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 200:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def jerk_result(message: types.Message,
                      state: FSMContext) -> None:
    """
    Adds jerk result to power table date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['jerk'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 200:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def split_jerk_result(message: types.Message,
                            state: FSMContext) -> None:
    """
    Adds split jerk result to power table date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 250:
            async with state.proxy() as data:
                data['split_jerk'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 250:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def thruster_result(message: types.Message,
                          state: FSMContext) -> None:
    """
    Adds thruster result to power table date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['jerk'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 250:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


async def cluster_result(message: types.Message,
                         state: FSMContext) -> None:
    """
    Adds cluster result to power table date and users telegram_id.
    :param message:
    :param state:
    :return:
    """
    try:
        if 25 <= float(message.text) <= 200:
            async with state.proxy() as data:
                data['jerk'] = round(float(message.text), ndigits=2)
                data['date'] = datetime.now()
            await db.update_power_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await power_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif float(message.text) > 250:
            await message.answer('Ого, силен! Скидывай видео в чат!')
        elif float(message.text) < 25:
            await message.answer('Что-то как-то не верится,'
                                 ' это же просто гриф!')
        else:
            await message.answer('Положительное число =)')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число!')


def register_power_handlers(dp: Dispatcher):
    dp.register_message_handler(long_jump_result,
                                state=PowerData.long_jump)
    dp.register_message_handler(snatch_result,
                                state=PowerData.snatch)
    dp.register_message_handler(power_snatch_result,
                                state=PowerData.power_snatch)
    dp.register_message_handler(hang_snatch_result,
                                state=PowerData.hang_snatch)
    dp.register_message_handler(hang_power_snatch_result,
                                state=PowerData.hang_power_snatch)
    dp.register_message_handler(clean_result,
                                state=PowerData.clean)
    dp.register_message_handler(power_clean_result,
                                state=PowerData.power_clean)
    dp.register_message_handler(power_jerk_result,
                                state=PowerData.power_jerk)
    dp.register_message_handler(jerk_result,
                                state=PowerData.jerk)
    dp.register_message_handler(split_jerk_result,
                                state=PowerData.split_jerk)
    dp.register_message_handler(thruster_result,
                                state=PowerData.thruster)
    dp.register_message_handler(cluster_result,
                                state=PowerData.cluster)
