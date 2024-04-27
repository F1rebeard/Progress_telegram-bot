import logging
import os
import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot, db

from keyboards.user_kb import (answer_week,
                               question_1,
                               question_2,
                               question_3,
                               question_4,
                               question_5,
                               question_6,
                               question_7)


class Questions(StatesGroup):
    workouts_volume = State()
    self_results = State()
    scaling = State()
    reduce = State()
    fatigue = State()
    recovery = State()
    general = State()


async def start_questions_about_workout_week():
    """
    Starts the question sequence about he passing week workouts.
    """
    users_to_ask = [368362025]
    for user in users_to_ask:
        await bot.send_message(
            text='Привет!\n\n'
            'Ответь пожалуйста на пару вопросов о тренировках'
            'этой недели 🤖',
            chat_id=user,
            reply_markup=answer_week
        )


async def ask_about_workout_volume(query: types.CallbackQuery,
                                   state: FSMContext):
    if query.data == 'do_the_answers':
        await query.message.edit_text(
            'Оцените объем нагрузки на этой неделе:',
            reply_markup=question_1
        )
        await query.answer()
        await state.set_state(Questions.workouts_volume)


async def get_volume_and_ask_for_results(query: types.CallbackQuery,
                                         state: FSMContext):
    """

    """
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['volume'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Оцените то, насколько субъективно'
                ' вы довольны результатами тренировок на этой неделе',
                reply_markup=question_2
            )
            await state.set_state(Questions.self_results)
            await query.answer()


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
                'Приходилось ли вам масштабировать задания?',
                reply_markup=question_3
            )
            await state.set_state(Questions.scaling)
            await query.answer()


async def get_scaling_and_ask_for_reducing(query: types.CallbackQuery,
                                           state: FSMContext):
    """

    """
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['scaling'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Убирали ли вы какие-то задания из программы?',
                reply_markup=question_4
            )
            await state.set_state(Questions.reduce)
            await query.answer()


async def get_reduce_and_ask_for_fatigue(query: types.CallbackQuery,
                                         state: FSMContext):
    """

    """
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['reducing'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Оцените уровень своего утомления и мышечной боли:',
                reply_markup=question_5
            )
            await state.set_state(Questions.fatigue)
            await query.answer()


async def get_fatigue_and_ask_about_recovery(query: types.CallbackQuery,
                                             state: FSMContext):
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['fatigue'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Оцените нетренировочные факторы: сон, питание и восстановление',
                reply_markup=question_6
            )
            await state.set_state(Questions.recovery)
            await query.answer()


async def get_recovery_and_ask_for_general(query: types.CallbackQuery,
                                           state: FSMContext):
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['recovery'] = user_answer
            await query.message.edit_text(
                'Окей\n\n'
                'Как вы чувствуете себя в целом?',
                reply_markup=question_7
            )
            await state.set_state(Questions.general)
            await query.answer()


async def get_general_and_add_data(query: types.CallbackQuery,
                                   state: FSMContext):
    if query.data.startswith('select_'):
        user_answer = int(query.data.split('_')[1])
        async with state.proxy() as data:
            data['general'] = user_answer
        await db.add_data_to_weekly_table(query.from_user.id, state)
        await state.finish()
        await query.message.edit_text('Данные добавлены!\n\n'
                                      'Спасибо за уделенное время!'
                                      'Графики своей активности можешь '
                                      'посмотреть в профиле!')
        await query.answer()


def register_question_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        ask_about_workout_volume,
        lambda query: True
    )
    dp.register_callback_query_handler(
        get_volume_and_ask_for_results,
        lambda query: True,
        state=Questions.workouts_volume
    )
    dp.register_callback_query_handler(
        get_results_and_ask_for_scaling,
        lambda query: True,
        state=Questions.self_results
    )
    dp.register_callback_query_handler(
        get_scaling_and_ask_for_reducing,
        lambda query: True,
        state=Questions.scaling
    )
    dp.register_callback_query_handler(
        get_reduce_and_ask_for_fatigue,
        lambda query: True,
        state=Questions.reduce
    )
    dp.register_callback_query_handler(
        get_fatigue_and_ask_about_recovery,
        lambda query: True,
        state=Questions.fatigue
    )
    dp.register_callback_query_handler(
        get_recovery_and_ask_for_general,
        lambda query: True,
        state=Questions.recovery
    )
    dp.register_callback_query_handler(
        get_general_and_add_data,
        lambda query: True,
        state=Questions.general
    )
