import logging
import re
from aiogram import types, Dispatcher
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, db
from keyboards.user_kb import (
    choose_levels, choose_kb, registration_keyboard, gender_keyboard,
    user_keyboard
)


class Registration(StatesGroup):
    new_user = State()
    payment = State()
    first_name = State()
    last_name = State()
    gender = State()
    email = State()
    training_level = State()


async def start_registration(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Start registration and asks for first name of user.
    :param query:
    :param state:
    :return:
    """
    if query.data == 'start_registration':
        await query.message.answer(text='Отлично!\n\nВведи своё имя:')
        await state.set_state(Registration.first_name)
        await query.answer()


async def get_first_name(message: types.Message, state: FSMContext) -> None:
    """
    Gets first name of user and asks for last name.
    :param message:
    :param state:
    :return:
    """
    if re.match(r"^[A-Z|А-ЯЁ][a-z|а-яё]{1,15}$", message.text):
        async with state.proxy() as data:
            data['first_name'] = message.text
        await bot.send_message(message.from_user.id,
                               text='Приятно познакомиться!\n\n'
                                    'А теперь фамилию:',
                               reply_markup=registration_keyboard)
        await state.set_state(Registration.last_name)
    else:
        await message.reply(
           text='Имя должно начинаться с большой буквы,'
                ' может состоять только из букв'
                ' и не превышать 15 символов'
        )


async def get_last_name(message: types.Message, state: FSMContext) -> None:
    """
    Get last name of user and asks for email.
    :param message:
    :param state:
    :return:
    """
    if re.match(r"^[A-Z|А-ЯЁ][a-z|а-яё]{1,25}$", message.text):
        async with state.proxy() as data:
            data['last_name'] = message.text
        await bot.send_message(message.from_user.id,
                               text='Хорошо, а теперь укажи свой пол:',
                               reply_markup=gender_keyboard)
        await bot.send_message(message.from_user.id,
                               text='Да, вот такой банальный вопрос',
                               reply_markup=registration_keyboard)
        await state.set_state(Registration.gender)
    else:
        await message.reply(
            text='Фамилия должна начинаться с большой буквы,'
                 ' может состоять только из букв'
                 'и не превышать 25 символов'
        )


async def choose_gender(query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Gets users gender and asks for email.
    :param query:
    :param state:
    :return:
    """
    if query.data in ['male', 'female']:
        user_gender = 'Мужской' if query.data == 'male' else 'Женский'
        await state.set_state(Registration.email)
        async with state.proxy() as data:
            data['gender'] = user_gender
        await bot.send_message(
            query.from_user.id,
            text='Отлично, осталось совсем чуть-чуть🥹 Напиши свой e-mail,'
                 ' пожалуйста:'
        )
        await query.answer()


async def get_email(message: types.Message, state: FSMContext):
    if re.match(r'^[\w.\-]{1,64}@\w+\.(by|ru|ua|com)$', message.text):
        async with state.proxy() as data:
            data['email'] = message.text
        user_level = await db.get_user_level(message.from_user.id)
        if user_level != 'Cтарт':
            await bot.send_message(
                message.from_user.id,
                text='Выбери свой уровень для тренировок 🥷',
                reply_markup=choose_kb
            )
            await bot.send_message(
                message.from_user.id,
                text='И на этом всё 👍',
                reply_markup=registration_keyboard)
            await state.set_state(Registration.training_level)
        else:
            async with state.proxy() as data:
                data['chosen_date'] = datetime.now().date()
            await db.user_start_final_registration(state, message.from_user.id)
            await bot.send_message(
                message.from_user.id,
                text='Регистрация выполнена! Спасибо 🙌\n\n Советую зайти в'
                     ' профиль 👹, раздел "Биометрика".\n\n Заполни его — эти'
                     ' данные пригодятся для автоматического подсчета веса на'
                     ' снарядах и упражнениях в некоторых тестах ㊗️',
                reply_markup=user_keyboard
            )
            await state.finish()
    else:
        await message.reply(text='Введите корректный email')


async def choose_workout_level(query: types.CallbackQuery,
                               state: FSMContext):
    """
    User is choosing his level during registration.
    :param query:
    :param state:
    :return:
    """
    level_to_answer = {
        'first_level': 'Первый',
        'second_level': 'Второй',
        'competition_level': 'Соревнования',
        'minkaif_level': 'Минкайфа',
        'start_level': 'Старт'
    }

    user_answer = level_to_answer.get(query.data)
    logging.info(f'Callback data: {query.data}')
    if user_answer is None:
        await query.message.answer(text='Вы не выбрали уровень',
                                   reply_markup=registration_keyboard)
    else:
        await query.answer(
            show_alert=True,
            text=f'Вы выбрали уровень "{user_answer}"',
        )
        async with state.proxy() as data:
            data['level'] = user_answer
            data['chosen_date'] = datetime.now().date()
        await db.user_final_registration(
            state=state,
            telegram_id=query.from_user.id
        )
        await state.finish()
        await bot.send_message(
            query.from_user.id,
            'Регистрация выполнена! Спасибо 🙌\n\n Советую зайти в профиль 👹,'
            ' раздел "Биометрика".\n\n Заполни его — эти данные пригодятся для'
            ' автоматического подсчета веса на снарядах и упражнениях в'
            ' некоторых тестах ㊗️',
            reply_markup=user_keyboard
        )


async def cancel_action(message: types.Message,
                        state: FSMContext):
    """
    Cancels FSMContext status
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.answer('Отменил')


def register_registration_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        start_registration,
        lambda query: True,
        state=Registration.new_user
    )
    dp.register_callback_query_handler(
        choose_workout_level,
        lambda query: True,
        state=Registration.training_level
    )
    dp.register_callback_query_handler(
        choose_gender,
        lambda query: True,
        state=Registration.gender
    )
    dp.register_message_handler(
        cancel_action,
        text='❌ Отмена',
        state='*'
    )
    dp.register_message_handler(
        get_first_name,
        state=Registration.first_name
    )
    dp.register_message_handler(
        get_last_name,
        state=Registration.last_name
    )

    dp.register_message_handler(
        get_email,
        state=Registration.email
    )
