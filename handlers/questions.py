import logging
import re
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound, BotBlocked


from create_bot import bot, db
from config.constants import ADMIN_IDS
from handlers.users import MainMenu
from keyboards.user_kb import (answer_week,
                               answer_question,
                               navigation_keyboard,
                               question_1,
                               question_2,
                               question_3)


class Questions(StatesGroup):
    workouts_volume = State()
    self_results = State()
    scaling = State()
    reduce = State()
    fatigue = State()
    recovery = State()
    general = State()


async def start_poll_for_time_in_progress():
    """
    Send a user message to start polling about his time in project.
    """
    active_users = await db.get_telegram_ids_of_active_users()
    answered_users = await db.get_telegram_ids_who_answered()
    users_to_ask = set(active_users) - set(answered_users)
    logging.info(f'Users to ask: {users_to_ask}')
    for user in users_to_ask:
        try:
            await bot.send_message(
                chat_id=user,
                text='Привет! \n\nМы собираем небольшую статистику'
                     ' по нашему проекту. Ответь пожалуйста на один вопрос 🥹',
                reply_markup=answer_question
            )
        except ChatNotFound or BotBlocked:
            logging.info(f'Нету чата с пользователем {user}')


async def start_questions_about_workout_week():
    """
    Starts the question sequence about the passing week workouts.
    """
    active_users = await db.get_telegram_ids_of_active_users()
    answered_users = await db.get_users_who_answered_about_this_week()
    logging.info(f'{answered_users}')
    users_to_ask = set(active_users) - set(answered_users) - set(ADMIN_IDS)
    logging.info(f'Users to ask: {users_to_ask}')
    for user in users_to_ask:
        try:
            await bot.send_message(
                text='Привет!\n\n'
                     'Ответь пожалуйста на несколько вопросов о тренировках '
                     'этой недели 🤖',
                chat_id=user,
                reply_markup=answer_week
            )
        except ChatNotFound or BotBlocked:
            logging.info(f'Чата с пользователем {user} нет!')


async def ask_about_week_self_results(query: types.CallbackQuery,
                                      state: FSMContext):
    if query.data == 'do_the_answers':
        await query.message.edit_text(
            'Оцените то, насколько'
            ' вы довольны результатами тренировок на этой неделе:',
            reply_markup=question_1
        )
        await query.answer()
        await state.set_state(Questions.self_results)


async def get_results_and_ask_for_scaling(query: types.CallbackQuery,
                                          state: FSMContext):
    """

    """
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['results'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Приходилось ли вам масштабировать или убирать задания'
                ' из программы?',
                reply_markup=question_2
            )
            await state.set_state(Questions.scaling)
            await query.answer()


async def get_scaling_and_ask_for_fatigue(query: types.CallbackQuery,
                                          state: FSMContext):
    """

    """
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['scaling'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Оцените уровень утомления и мышечной боли:',
                reply_markup=question_3
            )
            await state.set_state(Questions.fatigue)
            await query.answer()


async def get_fatigue_and_add_data(query: types.CallbackQuery,
                                   state: FSMContext):
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['fatigue'] = user_answer
        await db.add_data_to_weekly_table(query.from_user.id, state)
        await state.finish()
        await query.message.edit_text('Данные добавлены!\n\n'
                                      'Спасибо за уделенное время!\n\n'
                                      'Графики своей активности можешь '
                                      'посмотреть в профиле!')
        await query.answer()


async def ask_time_question(query: types.CallbackQuery,
                            state: FSMContext) -> None:
    """
    Ask about time in project and waiting for answer.
    """
    if query.data == 'answer_question':
        await query.message.answer(
            'Скажи как долго ты с нами? 🫶🏻🥹❤️‍🩹\n\n'
            'Напиши полную дату в формате'
            'ДД.ММ.ГГГГ\n\n Если не помнишь то напиши месяц и год начала'
            'тренировок в формате ММ.ГГГГ',
            reply_markup=navigation_keyboard
        )
        await state.set_state(MainMenu.ask_time_question)
        await query.answer()


async def get_answer_for_time_question(message: types.Message,
                                       state: FSMContext):
    """
    Receives answer from users and adds answer to database.
    :param message: answer from user
    :param state: if answered successfully state is finished.
    """
    telegram_id = message.from_user.id
    if re.match(
            r'^(?:(?:0?[1-9]|[12][0-9]|3[01])\.'
            r'(?:0?[1-9]|1[0-2])|(?:0?[1-9]|1[0-2]))\.(?:\d{4})$',
            message.text):
        try:
            date = datetime.strptime(message.text, "%d.%m.%Y")
            formatted_date = date.strftime('%Y-%m-%d')
        except ValueError:
            month, year = message.text.split('.')
            formatted_date = datetime.strptime(
                f'01.{month}.{year}', '%d.%m.%Y'
            ).strftime('%Y-%m-%d')
        await db.add_new_data_about_time_in_project(
            telegram_id, formatted_date
        )
        await message.answer(f'Данные добавлены\n\n'
                             f'Cпасибо, отличных тренировок!')
        await state.finish()
    else:
        await message.answer(
            'Неверный формат даты!\n\n'
            'Напиши полную дату в формате '
            'ДД.ММ.ГГГГ\n\n Если не помнишь день, то напиши месяц и год начала'
            'тренировок в формате ММ.ГГГГ'
        )


def register_question_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_results_and_ask_for_scaling,
        lambda query: True,
        state=Questions.self_results
    )
    dp.register_callback_query_handler(
        get_scaling_and_ask_for_fatigue,
        lambda query: True,
        state=Questions.scaling
    )
    dp.register_callback_query_handler(
        get_fatigue_and_add_data,
        lambda query: True,
        state=Questions.fatigue
    )
    dp.register_callback_query_handler(
        ask_time_question,
        lambda query: query.data == 'answer_question',
        state='*')
    dp.register_callback_query_handler(
        ask_about_week_self_results,
        state='*')
    dp.register_message_handler(get_answer_for_time_question,
                                state=MainMenu.ask_time_question)
