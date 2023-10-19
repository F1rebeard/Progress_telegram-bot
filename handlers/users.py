import logging
import os

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import State, StatesGroup

from config.constants import (ACTIVATIONS_BTNS,
                              EXERCISES_BTNS,
                              RELEASES_BTNS,
                              PREACTIVATIONS_BTNS,
                              STRETCHING_BTNS,
                              ABBREVIATIONS_DATA)
from graphic.graphic import characteristics_graphic
from graphic.formula import user_axis_value
from graphic.сonstants import (STRENGTH_RANGES,
                               STRENGTH_CAPACITY_RANGES,
                               AEROBIC_RANGES,
                               POWER_RANGES,
                               GYMNASTIC_RANGES,
                               METCON_RANGES)
from keyboards.user_kb import (user_keyboard,
                               profile_keyboard_1,
                               subscription_kb,
                               registration_button,
                               unfreeze_kb,
                               exercises_and_activations,
                               create_url_inline_keyboard
                               )
from keyboards.profile_kb import categories_keyboard
from keyboards.admin_kb import admin_keyboard
from handlers.registration import Registration
from config.constants import ADMIN_IDS
from create_bot import bot, db
from workout_clr.workout_calendar import calendar_callback as \
    workout_cal_callback, WorkoutCalendar


class MainMenu(StatesGroup):
    exercises = State()
    abbreviations = State()


async def start_bot(message: types.Message, state: FSMContext):
    """
    Start a keyboard for users or admins
    """
    telegram_id = message.from_user.id
    # проверяем если юзер админ
    # проверяем есть ли юзер в базе данных
    if await db.user_exists(telegram_id):
        try:
            # получаем дату действия подписки
            # завернуть в функцию проверки подписки
            subscription_date = await db.get_user_subscription_date(telegram_id)
            days_till_payment = (subscription_date - datetime.now().date()).days
            subscription_date = subscription_date.strftime("%d.%m.%Y")
            # Если являяется аодмином
            if telegram_id in ADMIN_IDS:
                await message.answer(
                    'Привет, повелитель {0.first_name}!'.format(message.from_user),
                    reply_markup=admin_keyboard
                )
            elif await db.check_freeze_status(telegram_id):
                await message.answer(text='Твоя подписка заморожена ❄️',
                                           reply_markup=unfreeze_kb)
            # Проверка срока подписки
            elif days_till_payment < 0:
                await message.answer(
                    f'Твоя подписка закончилась {subscription_date} '
                    f'😢😭. \n\n Чтобы не пропустить крутые тренировки -'
                    f' продли по кнопке ниже 😉',
                    reply_markup=subscription_kb
                )
            elif days_till_payment == 0:
                await message.answer(
                    f'Твоя подписка заканчивается сегодня! Чтобы не прерывать'
                    f' классные тренировки и убойные задания -'
                    f' продли подписку 😉',
                    reply_markup=user_keyboard
                )
            elif days_till_payment == 1:
                await message.answer(
                    f'Твоя подписка заканчивается завтра! Чтобы не прерывать'
                    f' классные тренировки и убойные задания -'
                    f' продли подписку 😉',
                    reply_markup=user_keyboard
                )
            else:
                await message.answer(
                    f'С возвращением!\n\n Твоя подписка заканчивается в '
                    f'течении {days_till_payment} дней. Отличных тренировок и '
                    f'прогресса в твоих результатах 🤙💪',
                    reply_markup=user_keyboard
                )
        except ValueError or TypeError:
            await message.answer('Нету данных о подписке!')
    # условие, что человек оплатил, но не выполнил регистрацию до конца.
    elif await db.user_payed_not_registered(telegram_id):
        await state.set_state(Registration.new_user)
        await message.answer(
            'Ты так и не закончил регистрацию, это займет пару минут',
            reply_markup=registration_button
        )
        await message.answer('Подписка уже оплачена, просто нужно ответить на'
                             'на пару вопросов по кнопке выше ☝️')
    else:
        await message.answer(
            f'Привет, {message.from_user.username}\n\n'
            f'Смотрю ты тут впервые! Если ты тут за тренировками в "Прогрессе",'
            f' то оплачивай подписку, проходи регистрацию и вперёд!',
            reply_markup=subscription_kb
        )


async def show_exercises(message: types.Message,
                         state: FSMContext):
    """
    Shows categories for exercises, stretching, releases for user.
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()
    if current_state is None:
        pass
    await state.set_state(state=MainMenu.exercises)
    await message.answer(
        text='Выбери категорию:',
        reply_markup=exercises_and_activations)


async def show_abbreviations(message: types.Message,
                             state: FSMContext):
    """
    Show abbreviations list for user.
    :param message:
    :param state:
    :return:
    """
    inline_kb = types.InlineKeyboardMarkup()
    #добавляем кнопки с сокращениями
    for abbreviation, (description, query_data) in ABBREVIATIONS_DATA.items():
        inline_kb.insert(
            types.InlineKeyboardButton(text=abbreviation,
                                       callback_data=query_data)
        )
    await state.set_state(state=MainMenu.abbreviations)
    await message.answer('Выберите сокращение:',
                         reply_markup=inline_kb)


async def send_description(query: types.CallbackQuery):
    """
    Show description for every abbreviation.
    :param query:
    :return:
    """
    query_data = [data for abbv, (desc, data) in ABBREVIATIONS_DATA.items()]
    if query.data in query_data:
        for abbv, (desc, data) in ABBREVIATIONS_DATA.items():
            if data == query.data:
                description = desc
                break
    await query.message.answer(text=description)
    await query.answer()


async def choose_exercise_category(query: types.CallbackQuery,
                                   state: FSMContext):
    """
    Open a chosen category with urls of exercises for user.
    :param query:
    :param state:
    :return:
    """
    if query.data == 'activations':
        inline_url_kb = create_url_inline_keyboard(ACTIVATIONS_BTNS)
        await bot.edit_message_text(text='Активации',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=inline_url_kb)

    elif query.data == 'preactivations':
        inline_url_kb = create_url_inline_keyboard(PREACTIVATIONS_BTNS)
        await bot.edit_message_text(text='Преактивации',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=inline_url_kb)
    elif query.data == 'stretching':
        inline_url_kb = create_url_inline_keyboard(STRETCHING_BTNS)
        await bot.edit_message_text(text='Растяжка',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=inline_url_kb)
    elif query.data == 'exercises':
        inline_url_kb = create_url_inline_keyboard(EXERCISES_BTNS)
        await bot.edit_message_text(text='Техника упражнений',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=inline_url_kb)
    elif query.data == 'release':
        inline_url_kb = create_url_inline_keyboard(RELEASES_BTNS)
        await bot.edit_message_text(text='Релиз',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=inline_url_kb)
    elif query.data == 'back':
        await bot.edit_message_text(text='Выбери категорию',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=exercises_and_activations)


async def show_profile_menu(message: types.Message,
                            state: FSMContext):
    """
    Pops up profile menu.
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()
    if current_state is None:
        pass
    if not await db.get_user_username(message.from_user.id):
        await db.insert_user_username(telegram_id=message.from_user.id,
                                      username=message.from_user.username)
    await message.answer('Вы зашли в свой профиль, где вы можете посмотреть'
                         ' и редактировать свои результаты и параметры.',
                         reply_markup=profile_keyboard_1)
    await message.answer('Выберите категорию для просмотра:',
                         reply_markup=categories_keyboard)


async def back_to_main_menu(message: types.Message, state: FSMContext):
    """
    Returns user back to main menu.
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.finish()
        logging.info('Cancelling state %r', current_state)
    if message.from_user.id in ADMIN_IDS:
        await message.answer('⬇ Главное меню ⬇', reply_markup=admin_keyboard)
    else:
        await message.answer('⬇ Главное меню ⬇', reply_markup=user_keyboard)


async def show_workout_calendar(message: types.Message,
                                state: FSMContext):
    """
    Pops ups workout calendar
    :param message:
    :param state:
    :return:
    """
    current_state = await state.get_state()
    if current_state is None:
        pass
    else:
        await state.finish()
        logging.info('Cancelling state %r', current_state)
    await bot.send_message(
        message.from_user.id,
        text='Выберите тренировку: ',
        reply_markup=await WorkoutCalendar().start_calendar(
            telegram_id=message.from_user.id
        )
    )


async def choose_date(
        query: types.CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext
):
    selected, date = await WorkoutCalendar().process_selection(
        query, callback_data)
    await WorkoutCalendar().day_action(query, callback_data, state)
    if selected:
        await db.update_chosen_date(query.from_user.id, date.date())
        telegram_id = query.from_user.id
        chosen_date = await db.get_chosen_date(telegram_id)
        workout_dates = await db.collect_workout_dates(telegram_id)
        if ((await db.check_subscription_status(telegram_id)) and
                (not await db.check_freeze_status(telegram_id))):
            if chosen_date in workout_dates:
                await query.message.answer(
                    text=f'Выбранный день - {date.strftime("%d.%m.%Y")}\n'
                    f'Действия:',
                    reply_markup=await WorkoutCalendar().chosen_day()
                )
                await query.answer()
            else:
                await query.message.answer(text='В этот день нет тренировки🏖️')
        elif await db.check_freeze_status(telegram_id):
            await query.message.answer(text='Твоя подписка заморожена ❄️',
                                       reply_markup=unfreeze_kb)
        else:
            await query.message.answer(text='Твоя подписка закончилась 💔',
                                       reply_markup=subscription_kb)
            await query.answer()


async def show_categories(message: types.Message,
                          state: FSMContext) -> None:
    """
    Pressing category buttons show all the categories.
    :param message:
    :param state:
    :return:
    """
    await state.finish()
    await bot.send_message(message.from_user.id,
                           f'{"Категории" : ^10}',
                           reply_markup=categories_keyboard)


async def show_users_graph(message: types.Message,
                           state: FSMContext) -> None:
    """
    Pressing buttons to show your graph
    :param message:
    :param state:
    :return:
    """
    user_id = message.from_user.id
    strength_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=STRENGTH_RANGES,
        user_results=await db.get_user_last_strength_result(
            telegram_id=user_id),
        category='Сила'
    )
    power_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=POWER_RANGES,
        user_results=await db.get_user_last_power_result(telegram_id=user_id),
        category='Взрывная сила'
    )
    aerobic_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=AEROBIC_RANGES,
        user_results=await db.get_user_last_aerobic_result(telegram_id=user_id),
        category='Выносливость и эргометры'
    )
    strength_capacity_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=STRENGTH_CAPACITY_RANGES,
        user_results=await db.get_user_last_strength_capacity_result(
            telegram_id=user_id),
        category='Силовая выносливость'
    )
    gymnastics_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=GYMNASTIC_RANGES,
        user_results=await db.get_user_last_gymnastics_result(
            telegram_id=user_id),
        category='Гимнастика'
    )
    metcon_result = await user_axis_value(
        telegram_id=user_id,
        characteristics_ranges=METCON_RANGES,
        user_results=await db.get_user_metcons_last_result(
            telegram_id=user_id),
        category='Метконы'
    )
    # Порядок в соотвествии с осями графика:
    # Cила, Взрывная сила, Силовая выносливость, Выносливость и эргометры,
    # Гимнастика и метконы

    user_values = [
        strength_result,
        power_result,
        strength_capacity_result,
        aerobic_result,
        gymnastics_result,
        metcon_result
    ]
    # создаем пустой список для незаполненных результатов
    not_fully_filled_data = []
    for result in user_values:
        if type(result) is str:
            not_fully_filled_data.append(result)
    if len(not_fully_filled_data) != 0:
        await message.answer(
            'Для получения своей характеристики необходимо заполнить следующие'
            ' упражнения:\n\n')
        for missing_movements in not_fully_filled_data:
            await message.answer(text=missing_movements)
    elif user_values[0] is None:
        await message.answer(
            'Вы же в Минкайфе - кайфуйте!\n\n'
            ' Зачем вам все эти графики?'
        )
    else:
        await message.answer(
            'Общий график характеристик на основе твоих результатов по всем '
            'категориям\n\nГрафик сейчас будет, джаст э момуемент'
        )
        await characteristics_graphic(user_values, user_id)
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=open(f'media/{user_id}.png', 'rb')
        )
        os.remove(f'media/{user_id}.png')




def register_users_handlers(dp: Dispatcher):
    """
    Registration of user handlers.
    """
    dp.register_message_handler(start_bot, commands=['start'])
    dp.register_callback_query_handler(choose_date,
                                       workout_cal_callback.filter(),
                                       state='*')
    dp.register_callback_query_handler(send_description,
                                       lambda query: True,
                                       state=MainMenu.abbreviations)
    dp.register_callback_query_handler(choose_exercise_category,
                                       lambda query: True,
                                       state=MainMenu.exercises)
    dp.register_message_handler(show_profile_menu, text='👹 Профиль',
                                state='*')
    dp.register_message_handler(back_to_main_menu, text='⏪ Главное меню',
                                state="*")
    dp.register_message_handler(show_exercises, text='🤓 Упражнения',
                                state='*')
    dp.register_message_handler(show_abbreviations, text='❓ Сокращения',
                                state='*'),
    dp.register_message_handler(show_workout_calendar, text='🏋 Тренировки',
                                state='*')
    dp.register_message_handler(show_categories, text='🦄️ Категории',
                                state='*')
    dp.register_message_handler(show_users_graph,
                                text='📊 Твои характеристики',
                                state='*')
