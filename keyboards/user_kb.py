from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

CHOOSE_LEVEL_BTN = (
    ('Первый 🏋️', 'first_level'),
    ('Второй 👹', 'second_level'),
    ('Минкайфа 🦖', 'minkaif_level'),
    ('Соревнования 🥷', 'competition_level'),
)

CHOSEN_DAY_BTNS = (
    ('Получить задание 🏋️‍♂️', 'get_workout'),
    ('Записать результат ✏️', 'workout_result'),
    ('Посмотреть результаты остальных 🕵️‍♂️', 'athletes_results')
)

CHOOSE_SUBSCRIPTION = (
    ('30 дней без куратора 🦁', 'one_month_sub'),
    ('30 дней с куратором 🐺🦁', 'one_month_sub_plus'),
    ('"Старт" 30 дней программы 👨‍🚀', 'one_month_start'),
    ('"Cтарт" полная программа 👨‍🚀🤖‍🚀', 'full_start')
)

CHOSE_EXERCISE_CATEGORY = (
    ('Активации', 'activations'),
    ('Предактивации', 'preactivations'),
    ('Растяжка', 'stretching'),
    ('Релиз', 'release'),
    ('Техника упражнений', 'exercises'),
)

QUESTION_1 = (
    ('Вообще не доволен', 'select_1'),
    ('Скорее доволен', 'select_2'),
    ('Скорее, доволен', 'select_3'),
    ('Доволен', 'select_4'),
    ('Очень доволен', 'select_5')
)

QUESTION_2 = (
    ('Нет, всё как есть', 'select_1'),
    ('Масштабировал или убрал 1-2 задания', 'select_2'),
    ('Масштабировал или убрал 3-4 задания', 'select_3'),
    ('Масштабировал или убрал больше 4 заданий', 'select_4')
)

QUESTION_3 = (
    ('Мышцы болят так, что сложно в обычной жизни', 'select_1'),
    ('Мышцы болят', 'select_2'),
    ('Мышцы слегка побаливают', 'select_3'),
    ('Мышцы немного ощущаются, а так норм', 'select_4'),
    ('Отличное самочувствие, свежий, ничего не болит', 'select_5')
)

# main menu buttons
workout_button = KeyboardButton('🏋 Тренировки')
excercises_button = KeyboardButton('🤓 Упражнения')
abbreviations_button = KeyboardButton('❓ Сокращения')
tests_button = KeyboardButton('📉 Тесты')
profile_button = KeyboardButton('👹 Профиль')
subscription_button = KeyboardButton('⏳🈂 Подписка')
unfreeze_button = KeyboardButton('❄️ Разморозка')

# navigation buttons
backward_button = KeyboardButton('⬅ Назад')
main_menu_button = KeyboardButton('⏪ Главное меню')
cancel_button = KeyboardButton('❌ Отмена')

# profile_buttons
full_graphic_button = KeyboardButton('🥷🏿☯ Полная характеристика')
base_graphic_button = KeyboardButton('🐯🐾 Базовая характеристика')
add_profile_button = KeyboardButton('🔄 Редактировать')
categories_button = KeyboardButton('🦄️ Категории')

user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                    row_width=2).add(
    workout_button,
    profile_button,
    tests_button,
    excercises_button,
    abbreviations_button,
    subscription_button
)

registration_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                            row_width=2).add(
    cancel_button
)

profile_keyboard_1 = ReplyKeyboardMarkup(resize_keyboard=True,
                                         row_width=2).add(
    categories_button,
    main_menu_button,
    base_graphic_button,
    full_graphic_button,
    cancel_button
)

profile_keyboard_2 = ReplyKeyboardMarkup(resize_keyboard=True,
                                         row_width=3).add(
    cancel_button,
    categories_button,
    main_menu_button
)

navigation_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                                          row_width=3).add(
    backward_button,
    cancel_button,
    main_menu_button
)

subscription_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    subscription_button)

unfreeze_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    unfreeze_button)


# choose workout level inline keyboard
def create_inline_keyboard(buttons: tuple) -> InlineKeyboardMarkup:
    """
    Creates filled inline_keyboard with prepared buttons
    :param buttons: Tuple of buttons and query data
    :return:
    """
    keyboard = InlineKeyboardMarkup()
    for text, data in buttons:
        keyboard.add(
            InlineKeyboardButton(text, callback_data=data)
        )
    return keyboard


def create_url_inline_keyboard(buttons: tuple) -> InlineKeyboardMarkup:
    """
    Create inline keyboard with urls and back button.
    :param buttons:
    :return:
    """
    back_button = InlineKeyboardButton(text='Назад', callback_data='back')
    inline_kb = InlineKeyboardMarkup()
    inline_kb.row(back_button)
    for text, url in buttons:
        inline_kb.row(InlineKeyboardButton(text=text, url=url))
    return inline_kb


def get_choose_level_data(buttons: tuple) -> list:
    level_data = []
    for levels in buttons:
        level_data.append(levels[1])
    return level_data


# inline keyboard for chosen date in workout calendar
chosen_date_kb = create_inline_keyboard(CHOSEN_DAY_BTNS)

registration_button = create_inline_keyboard(
    (('Закончить регистрацию 🦄', 'start_registration'),))

gender_keyboard = create_inline_keyboard(
    (('Женский 🏋🏻‍♀️', 'female'), ('Мужской 🏋🏻', 'male'))
)

answer_question = create_inline_keyboard(
    (('Да, с удовольствием отвечу 🦄', 'answer_question'),)
)

# inline keyboards for questions about the workout week
answer_week = create_inline_keyboard(
    (('Рассказать о прошедшей неделе', 'do_the_answers'),)
)

question_1 = create_inline_keyboard(QUESTION_1)
question_2 = create_inline_keyboard(QUESTION_2)
question_3 = create_inline_keyboard(QUESTION_3)

# inline keyboard for choosing level during registration
choose_kb = create_inline_keyboard(CHOOSE_LEVEL_BTN)

# text list for callback query after choosing level during registration
choose_levels = get_choose_level_data(CHOOSE_LEVEL_BTN)

# inline keyboard for choosing subscription
choose_sub = create_inline_keyboard(CHOOSE_SUBSCRIPTION)

# exercises and activations for user
exercises_and_activations = create_inline_keyboard(CHOSE_EXERCISE_CATEGORY)


def callback_answers_for_choose_levels(chosen_level) -> str:
    """
    Returns callback query data as chosen level for user, during registration.
    """
    levels = choose_levels
    if chosen_level in levels:
        return chosen_level
