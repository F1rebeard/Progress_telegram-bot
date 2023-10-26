from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards import profile_kb


MOVEMENTS_CONNECTION = {
    'Становая 70% от 1ПМ на кол-во': 'Cтановая тяга 1ПМ',
    'Присед 70% от 1ПМ на кол-во': 'Присед 1ПМ',
    'Жим стоя 70% от 1ПМ на кол-во': 'Жим стоя 1ПМ',
    'Жим лежа 70% от 1ПМ на кол-во': 'Жим лежа 1ПМ',
}

GYMNASTICS_CONNECTION = {
    'Подтягивания с подвесом на кол-во': 'Строгие подтягивания 1ПМ',
    'Отжимания  с подвесом на кол-во муж': 'Строгие подтягивания 1ПМ',
    'Отжимания  с подвесом на кол-во жен': 'Строгие подтягивания 1ПМ',
}


class StrengthCapacityData(StatesGroup):
    deadlift = State()
    squat = State()
    push_press = State()
    bench_press = State()
    pull_ups = State()
    deeps = State()


async def weight_for_movement(telegram_id: int, movement: str) -> int or str:
    """
    Count a 70% weight from 1RM movement
    :param movement:
    :param telegram_id:
    :return:
    """
    try:
        biometrics = list(await db.get_user_biometrics(telegram_id))
        user_weight = biometrics[3]
        user_gender = biometrics[1]
        if movement in list(MOVEMENTS_CONNECTION.keys()):
            strength_movement_rms = await db.strength_movement_result_history(
                telegram_id, MOVEMENTS_CONNECTION.get(movement))
            weight = round(float(strength_movement_rms[0][1]) * 0.7, 3)
        elif movement == 'Подтягивания с подвесом на кол-во':
            pull_up_rms = await db.gymnastics_result_history(
                telegram_id, GYMNASTICS_CONNECTION.get(movement))
            weight = round(
                (((float(pull_up_rms[0][1]) + user_weight)) * 0.7) - user_weight
            )
            if weight < 0:
                return 0
        elif movement == 'Отжимания  с подвесом на кол-во':
            if user_gender == 'Женский':
                deep_rms = await db.gymnastics_result_history(
                    telegram_id, 'Отжимания на брусьях 1ПМ'
                )
            if user_gender == 'Мужской':
                deep_rms = await db.gymnastics_result_history(
                    telegram_id, 'Отжимания на брусьях 1ПМ'
                )
            weight = round(
                (((float(
                    deep_rms[0][1]) + user_weight)) * 0.7) - user_weight
            )
            if weight < 0:
                return 0
        return int(weight)
    except TypeError or ValueError:
        return 'Нету данных!'


async def sinkler_coef(telegram_id: int, movement: str, reps: int) -> float:
    """
    For movement in strength capacity.
    koeff = reps * weight / user_weight.
    :return:
    """
    user_weight = list(await db.get_user_biometrics(telegram_id))[3]
    movement_weight = await weight_for_movement(telegram_id, movement)
    if movement in list(MOVEMENTS_CONNECTION.keys()):
        koefficent = int(reps) * movement_weight / float(user_weight)
    elif movement in ['Подтягивания с подвесом на кол-во',
                      'Отжимания  с подвесом на кол-во']:
        if movement_weight == 0:
            koefficent = int(reps)
            return round(koefficent, 2)
        koefficent = int(reps) * movement_weight
    return round(koefficent, 2)


async def deadlift_cpt_result(
        message: types.Message,
        state: FSMContext) -> None:
    """
    Adds reps for 70% 1RM deadlift test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 3 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Сильно круто, лимит 75!')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


async def squat_cpt_result(message: types.Message, state: FSMContext) -> None:
    """
    Adds reps for 70% 1RM squat test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 3 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Cильно круто, лимит 75!')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


async def push_press_cpt_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds reps for 70% 1RM push press test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 3 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Cильно круто, лимит 75!')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


async def bench_press_cpt_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Adds reps for 70% 1RM bench_press test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 3 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Cильно круто, лимит 75!')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


async def pull_up_cpt_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Add reps for [ulls ups capaicty test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 2 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Cильно круто, лимит 75!')
        elif 0 < int(message.text) < 2:
            await message.answer('Я знаю, ты можешь сделать 2 раза точно!\n'
                                 'Если что - бери резинку')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


async def deeps_cpt_result(
        message: types.Message,
        state: FSMContext
) -> None:
    """
    Add reps for [ulls ups capaicty test.
    :param message:
    :param state:
    :return:
    """
    try:
        if 3 <= int(message.text) <= 75:
            async with state.proxy() as data:
                data['reps'] = int(message.text)
                data['movement_weight'] = await weight_for_movement(
                    message.from_user.id, data['movement']
                )
                data['koef'] = await sinkler_coef(
                    message.from_user.id,
                    data['movement'],
                    data['reps']
                )
                data['date'] = datetime.now()
            await db.update_strength_capacity_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.strength_capacity_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif int(message.text) > 75:
            await message.answer('Cильно круто, лимит 75!')
        else:
            await message.answer('Введи положительное число!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести положительное число!')


def register_strength_capacity_handlers(dp: Dispatcher):
    dp.register_message_handler(deadlift_cpt_result,
                                state=StrengthCapacityData.deadlift)
    dp.register_message_handler(squat_cpt_result,
                                state=StrengthCapacityData.squat)
    dp.register_message_handler(push_press_cpt_result,
                                state=StrengthCapacityData.push_press)
    dp.register_message_handler(bench_press_cpt_result,
                                state=StrengthCapacityData.bench_press)
    dp.register_message_handler(pull_up_cpt_result,
                                state=StrengthCapacityData.pull_ups)
    dp.register_message_handler(deeps_cpt_result,
                                state=StrengthCapacityData.deeps)
