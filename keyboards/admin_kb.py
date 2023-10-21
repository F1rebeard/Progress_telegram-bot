from datetime import datetime
from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)

from keyboards.user_kb import create_inline_keyboard

#inline buttons for actions with selected users
ACTIONS_WITH_CHOSEN_USERS = (
    ('⚛ Сменить уровень', 'change_level_of_user'),
    ('🆗 Добавить подписку', 'add_subscription'),
    ('🥶 Заморозить подписку', 'freeze_subscription'),
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

# admin menu buttons
users_button = KeyboardButton('👫 Операции с атлетами')
inactive_users_button = KeyboardButton('👥 Неактивные пользователи')
send_to_all_button = KeyboardButton('📢 Сообщение всем')
add_workouts = KeyboardButton('⏬ Добавить новые тренировки')
delete_workouts = KeyboardButton('⚠️ Удалить последнюю неделю тренировок')

# navigation buttons
main_menu_button = KeyboardButton('⏪ Главное меню')
back_button = KeyboardButton('⬅ Назад')

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    admin_button,
    workout_button,
    profile_button,
    excercises_button,
    abbreviations_button,
)

admin_tools = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    users_button,
    inactive_users_button,
    send_to_all_button,
    add_workouts,
    delete_workouts,
    main_menu_button
)


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
            print(user_info[0])
        else:
            keyboard.add(
                InlineKeyboardButton(
                    f'{user_info[1]} {user_info[2]} '
                    f'📆❌= {days_till_end}',
                    callback_data=user_info[0]
                )
            )
            print(user_info[0])
    return keyboard

