from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import db
from keyboards import profile_kb


class GymnasticsData(StatesGroup):
    pull_up_one_rm = State()
    ring_deep_one_rm = State()
    deep_one_rm = State()
    pull_ups = State()
    strict_hs_push_ups = State()
    hs_push_ups = State()
    strict_ring_muscle_ups = State()
    ring_muscle_ups = State()
    time_ring_muscle_ups = State()
    muscle_ups = State()
    time_muscle_ups = State()
    toes_to_bar = State()
    ropes = State()
    legless_ropes = State()
    l_sit = State()
    hang_l_sit = State()
    hang = State()
    hs_walk = State()
    time_hs_walk = State()


async def pull_up_one_rm_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds 1 rm pull up result to gymnastics table.
    :param message:
    :param state:
    :return:
    """
    try:
        weight = int(message.text)
        if 0 <= weight <= 100:
            async with state.proxy() as data:
                data['result'] = weight
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif weight > 100:
            await message.answer('Какая-то гравитационная аномалия?!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100')


async def rings_deep_one_rm_result(message: types.Message,
                                   state: FSMContext) -> None:
    """
    Adds 1 rm rings deep result to gymnastics table.
    :param message:
    :param state:
    :return:
    """
    try:
        weight = int(message.text)
        if 0 <= weight <= 100:
            async with state.proxy() as data:
                data['result'] = weight
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif weight > 100:
            await message.answer('Какая-то гравитационная аномалия?!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100')


async def deep_one_rm_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds 1 rm deep result to gymnastics table.
    :param message:
    :param state:
    :return:
    """
    try:
        weight = int(message.text)
        if 0 <= weight <= 100:
            async with state.proxy() as data:
                data['result'] = weight
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif weight > 100:
            await message.answer('Какая-то гравитационная аномалия?!')
    except ValueError or TypeError:
        await message.answer('Нужно ввести число! Например 100.5')


async def pull_ups_result(message: types.Message, state: FSMContext) -> None:
    """
    Adds pull ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 150:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 150:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def strict_hs_push_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict handstand push ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 100:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 100:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def hs_push_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds handstand push ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 100:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 100:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def strict_ring_muscle_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 30:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 30:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def ring_muscle_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 50:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 50:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def time_ring_muscle_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 50:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 50:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def muscle_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 50:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 50:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def time_muscle_ups_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 50:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 50:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def toes_to_bar_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 100:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 100:
            await message.answer('Что-то фантастическое, мультипликационное!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def ropes_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 30:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 30:
            await message.answer('Тарзан, это ты?')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def legless_ropes_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        reps = int(message.text)
        if 0 <= reps <= 30:
            async with state.proxy() as data:
                data['result'] = reps
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif reps > 30:
            await message.answer('Тарзан, это ты?')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def l_sit_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        seconds = int(message.text)
        if 0 <= seconds <= 300:
            async with state.proxy() as data:
                data['result'] = seconds
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif seconds > 300:
            await message.answer('Cтальной пресс, или магия рептилий?')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def hang_l_sit_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        seconds = int(message.text)
        if 0 <= seconds <= 300:
            async with state.proxy() as data:
                data['result'] = seconds
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif seconds > 300:
            await message.answer('Cтальной пресс, или магия рептилий?')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def hang_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        seconds = int(message.text)
        if 0 <= seconds <= 1200:
            async with state.proxy() as data:
                data['result'] = seconds
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif seconds > 1200:
            await message.answer('Не хват, а крюк какой-то!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def hs_walk_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        meters = int(message.text)
        if 0 <= meters <= 100:
            async with state.proxy() as data:
                data['result'] = meters
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif meters > 1200:
            await message.answer('Ноги-руки, или руки-ноги!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


async def time_hs_walk_result(
        message: types.Message, state: FSMContext) -> None:
    """
    Adds strict rings muscle ups result to gymnastics data:
    :param message:
    :param state:
    :return:
    """
    try:
        meters = int(message.text)
        if 0 <= meters <= 100:
            async with state.proxy() as data:
                data['result'] = meters
                data['date'] = datetime.now()
            await db.update_gymnastics_movement(state)
            await message.answer(
                f'Данные обновлены!',
                reply_markup=await profile_kb.gymnastics_inline_keyboard(
                    message.from_user.id
                )
            )
            await state.finish()
        elif meters > 100:
            await message.answer('Ноги-руки, или руки-ноги!')
    except ValueError or TypeError:
        await message.answer('Нужно  целое положительное число! Например: 8')


def register_gymnastics_handlers(dp: Dispatcher):
    dp.register_message_handler(pull_up_one_rm_result,
                                state=GymnasticsData.pull_up_one_rm)
    dp.register_message_handler(rings_deep_one_rm_result,
                                state=GymnasticsData.ring_deep_one_rm)
    dp.register_message_handler(deep_one_rm_result,
                                state=GymnasticsData.deep_one_rm)
    dp.register_message_handler(pull_ups_result,
                                state=GymnasticsData.pull_ups)
    dp.register_message_handler(strict_hs_push_ups_result,
                                state=GymnasticsData.strict_hs_push_ups)
    dp.register_message_handler(hs_push_ups_result,
                                state=GymnasticsData.hs_push_ups)
    dp.register_message_handler(strict_ring_muscle_ups_result,
                                state=GymnasticsData.strict_ring_muscle_ups)
    dp.register_message_handler(ring_muscle_ups_result,
                                state=GymnasticsData.ring_muscle_ups)
    dp.register_message_handler(time_ring_muscle_ups_result,
                                state=GymnasticsData.time_ring_muscle_ups)
    dp.register_message_handler(muscle_ups_result,
                                state=GymnasticsData.muscle_ups)
    dp.register_message_handler(time_muscle_ups_result,
                                state=GymnasticsData.time_muscle_ups)
    dp.register_message_handler(toes_to_bar_result,
                                state=GymnasticsData.toes_to_bar)
    dp.register_message_handler(ropes_result,
                                state=GymnasticsData.ropes)
    dp.register_message_handler(legless_ropes_result,
                                state=GymnasticsData.legless_ropes)
    dp.register_message_handler(l_sit_result,
                                state=GymnasticsData.l_sit)
    dp.register_message_handler(hang_l_sit_result,
                                state=GymnasticsData.hang_l_sit)
    dp.register_message_handler(hang_result,
                                state=GymnasticsData.hang)
    dp.register_message_handler(hs_walk_result,
                                state=GymnasticsData.hs_walk)
    dp.register_message_handler(time_hs_walk_result,
                                state=GymnasticsData.time_hs_walk)
