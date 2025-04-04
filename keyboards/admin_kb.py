import logging
from datetime import datetime
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

from keyboards.user_kb import create_inline_keyboard, tests_button

#inline buttons for actions with selected users
ACTIONS_WITH_CHOSEN_USERS = (
    ('⚛ Сменить уровень', 'change_level_of_user'),
    ('🆗 Добавить подписку', 'add_subscription'),
    ('🥶 Заморозить подписку', 'freeze_subscription'),
    ('🦉 Назначить куратора', 'add_curator'),
    ('📈 Еженедельная динамика', 'weekly_dynamic'),
    ('🤬 Отменить подписку', 'cancel_subscription'),
    ('💬 Отправить сообщение', 'send_message_via_bot'),
)

YES_OR_NO_INLINE = (
    ('Да 🤝', 'yes_action'),
    ('Нет ✋', 'no_action')
)

yes_or_no_inline_kb = create_inline_keyboard(YES_OR_NO_INLINE)

user_action_inline_kb = create_inline_keyboard(ACTIONS_WITH_CHOSEN_USERS)

# user buttons
workout_button = KeyboardButton('🏋 Тренировки')
excercises_button = KeyboardButton('🤓 Упражнения')
abbreviations_button = KeyboardButton('❓ Сокращения')
profile_button = KeyboardButton('👹 Профиль')
subscription_button = KeyboardButton('⏳🈂 Подписка')

# admin buttons
admin_button = KeyboardButton('🧙 Aдминка')

# curator buttons
curator_button = KeyboardButton('👥 Мои атлеты')

# admin menu buttons
users_button = KeyboardButton('👫 Операции с атлетами')
inactive_users_button = KeyboardButton('👥 Неактивные пользователи')
add_new_users_button = KeyboardButton('👤 Добавить нового пользователя')
send_to_all_button = KeyboardButton('📢 Сообщение всем')
add_workouts = KeyboardButton('⏬ Добавить новые тренировки')
delete_workouts = KeyboardButton('⚠️ Удалить последнюю неделю тренировок')

# navigation buttons
main_menu_button = KeyboardButton('⏪ Главное меню')
back_button = KeyboardButton('⬅ Назад')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    admin_button,
    workout_button,
    tests_button,
    profile_button,
    excercises_button,
    abbreviations_button,
)

curator_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    curator_button,
    workout_button,
    tests_button,
    profile_button,
    excercises_button,
    abbreviations_button,
    subscription_button
)

admin_tools = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    users_button,
    inactive_users_button,
    add_new_users_button,
    send_to_all_button,
    add_workouts,
    delete_workouts,
    main_menu_button
)


def string_ids_into_list(telegram_ids: str) -> list:
    """
    Takes a string with telegram_ids separeted my ',' and return back list
    of these ids.
    """
    if telegram_ids is None or telegram_ids == '':
        # пустой список
        return []
    else:
        if ',' in telegram_ids:
            result = [int(x) for x in telegram_ids.split(',') if x != '']
            return result
        elif len(telegram_ids) == 1:
            result = [int(telegram_ids)]
            return result


async def curators_inline_kb(curators_list: list) -> InlineKeyboardMarkup:
    """
    Returns inline keyboard with curators.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    for curator in curators_list:
        athletes_sum = len(string_ids_into_list(curator[4]))
        keyboard.add(InlineKeyboardButton(
            f'{curator[1]} {curator[2]} 🏋🏻={athletes_sum}',
            callback_data=f'cura_{curator[0]}'
        ))
    return keyboard


async def users_info_inline_kb(chosen_users: list) -> InlineKeyboardMarkup:
    """
    :param chosen_users:
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    # user_info[0] - telegram_id
    # user_info[1] - first_name
    # user_info[2] - last_name
    # user_info[3] - level
    # user_info[4] - subscription_date
    for user_info in chosen_users:
        sub_date = datetime.strptime(user_info[4], "%Y-%m-%d").date()
        days_till_end = (sub_date - datetime.now().date()).days
        if days_till_end > 0:
            keyboard.add(
                InlineKeyboardButton(
                    f'{user_info[1]} {user_info[2]} '
                    f'📆✅= {days_till_end}',
                    callback_data=user_info[0]
                )
            )
        else:
            keyboard.add(
                InlineKeyboardButton(
                    f'{user_info[1]} {user_info[2]} '
                    f'📆❌= {days_till_end}',
                    callback_data=user_info[0]
                )
            )
    return keyboard


async def inactive_users_inline_kb(chosen_users: list) -> InlineKeyboardMarkup:
    """
    :param chosen_users:
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    # user_info[0] - telegram_id
    # user_info[1] - first_name
    # user_info[2] - last_name
    # user_info[3] - level
    # user_info[4] - subscription_date
    for user_info in chosen_users:
        sub_date = datetime.strptime(user_info[4], "%Y-%m-%d").date()
        days_till_end = (sub_date - datetime.now().date()).days
        if days_till_end > -30:
            keyboard.add(
                InlineKeyboardButton(
                    f'{user_info[1]} {user_info[2]} '
                    f'📆❌= {days_till_end}',
                    callback_data=user_info[0]
                )
            )
    return keyboard
