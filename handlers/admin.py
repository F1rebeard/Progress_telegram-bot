import logging
import os

from datetime import datetime, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import ChatNotFound

from dotenv import load_dotenv

from config.constants import ADMIN_IDS, BACKUP_ID
from graphic.graphic import (user_weekly_dynamic_graph,
                             levels_weekly_dynamic_graph,
                             get_users_ages_and_mean_ages,
                             ages_of_users_histogram,
                             months_in_project_histogram
                             )
from keyboards.admin_kb import (admin_tools,
                                users_info_inline_kb,
                                user_action_inline_kb,
                                yes_or_no_inline_kb)
from keyboards.user_kb import choose_kb, question_1
from handlers.users import back_to_main_menu
from handlers.questions import Questions
from database.workouts_from_sheet import (
    get_data_from_google_sheet,
    delete_workouts_from_database,
)
from create_bot import bot, db
from workout_clr.workout_calendar import ChosenDateData

load_dotenv()

JSON_PATH = os.getenv('JSON_PATH')
SHEET_TITLE = os.getenv('SHEET_TITLE')


class UsersInfo(StatesGroup):
    find_users = State()
    user_management = State()
    inactive_user_managment = State()
    actions_on_user = State()
    change_level = State()
    add_subscription = State()
    cancel_subscription = State()
    send_message_via_bot = State()
    send_to_all_via_bot = State()
    approval = State()
    upload_workouts = State()
    delete_workouts = State()
    freeze_subscription = State()
    unfreeze_subscription = State()
    add_new_user = State()


async def backup_database():
    """
    Makes a backup of database.
    """
    db_path = 'database/progress.db'
    if os.path.exists(db_path):
        db_backup = f'{db_path}.bak'
        try:
            # Copy the database file to create a backup
            os.makedirs(os.path.dirname(db_backup), exist_ok=True)
            with open(db_path, 'rb') as src, open(db_backup, 'wb') as dst:
                dst.write(src.read())

            # Send the backup file via Telegram
            with open(db_backup, 'rb') as file:
                await bot.send_document(chat_id=BACKUP_ID,
                                        document=types.InputFile(
                                            file,
                                            filename='database_backup.db'))
        except Exception as e:
            await bot.send_message(
                chat_id=BACKUP_ID,
                text=f"Error creating database backup: {str(e)}")
    else:
        await bot.send_message(
            chat_id=BACKUP_ID,
            text="Database file not found.")


async def send_birthday_users():
    birthdays = await db.get_today_birthday_users()
    logging.info(f'Дни рождения завтра {birthdays}')
    if len(birthdays) > 0:
        text_for_one = (f'День Рождения завтра 🎉🎂✨🍰🥳\n\n'
                        f'@{birthdays[0][0]}\n'
                        f'{birthdays[0][1]} {birthdays[0][2]}')
        text_for_many = f'День Рождения завтра 🎉🎂✨🍰🥳\n\n'
        for admin in ADMIN_IDS:
            for user in birthdays:
                text_for_many += (f'@{user[0]}\n'
                                  f'{user[1]} {user[2]}\n\n')
            if len(birthdays) > 1:
                await bot.send_message(
                    chat_id=admin,
                    text=text_for_many
                )
            if len(birthdays) == 1:
                await bot.send_message(
                    chat_id=admin,
                    text=text_for_one
                )
    else:
        pass


async def users_management(users_info: list) -> dict:
    """
    Transforms tuple from database to dict to identify user by his telegram_id.
    :param users_info:
    :return:
    """
    result = {}
    for user_info in users_info:
        # user_info[0] - telegram_id
        # user_info[1] - first_name
        # user_info[2] - last_name
        # user_info[3] - level
        # user_info[4] - subscription date
        # user_info[5] - username in telegram
        # user_info[6] - registration_date
        # user_info[7] - birthdate
        result.update({int(user_info[0]): [user_info[1:7]]})
    return result


async def users_data_for_admin():
    users_data = await db.get_users_data()
    active_users = len(users_data)
    male = []
    female = []
    first_lvl = []
    second_lvl = []
    # соревновательный уровень
    start_lvl = []
    third_lvl = []
    minkaifa_lvl = []
    frozen_users = []
    # получаем list of tuple
    for user in users_data:
        # user[0] - gender
        # user[1] - level
        # user[2] - sub_status
        # user[3] - freeze_status
        if user[0] == 'Женский':
            female.append(user)
        if user[0] == 'Мужской':
            male.append(user)
        if user[1] == 'Первый':
            first_lvl.append(user)
        if user[1] == 'Второй':
            second_lvl.append(user)
        if user[1] == 'Минкайфа':
            minkaifa_lvl.append(user)
        if user[1] == 'Соревнования':
            third_lvl.append(user)
        if user[1] == 'Старт':
            start_lvl.append(user)
        if user[3]:
            frozen_users.append(user)
    logging.info(f'Заморозка у {len(frozen_users)}')
    return (active_users,
            len(frozen_users),
            len(male),
            len(female),
            len(first_lvl),
            len(second_lvl),
            len(minkaifa_lvl),
            len(third_lvl),
            len(start_lvl),)


async def show_administration_tools(message: types.Message,
                                    state: FSMContext,) -> None:
    """
     Show admin tools after clicking admin button
    """
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is None:
            pass
        else:
            await state.finish()
        # preparing graph with ages of users
        men_data, women_data = await db.get_birthdate_of_active_users()
        men_age, men_mean_age = get_users_ages_and_mean_ages(men_data)
        women_age, women_mean_age = get_users_ages_and_mean_ages(women_data)
        await ages_of_users_histogram(
            men_age, women_age, men_mean_age, women_mean_age
        )

        # months in projects vote results
        await months_in_project_histogram()

        # weekly dynamic for all users by levels
        await levels_weekly_dynamic_graph()

        # sending photos with graphics
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=open(f'media/users_ages.png', 'rb'),
            caption='Статистика по возрастам'
        )
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=open(f'media/time_in_project_hist.png', 'rb'),
            caption='Продолжительность подписки в "Прогрессе"'
        )
        await bot.send_photo(
            chat_id=message.from_user.id,
            photo=open(f'media/levels_weekly.png', 'rb'),
            caption='Еженедельная динамика по уровням'
        )
        # removing files
        os.remove(f'media/users_ages.png')
        os.remove(f'media/time_in_project_hist.png')
        os.remove(f'media/levels_weekly.png')

        await message.answer(
            text='Выбери действия, повелитель:',
            reply_markup=admin_tools
        )


async def find_users_by_names(message: types.Message, state: FSMContext):
    """
    Show admin tools for working with users.
    """
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is None:
            pass
        else:
            await state.finish()
        logging.info('Cancelling state %r', current_state)
        users_data = await users_data_for_admin()
        await state.set_state(state=UsersInfo.find_users)
        await message.answer(
            text=f'Статистика:\n\n'
                 f'Всего активных атлетов 🥵 - {users_data[0]}\n'
                 f'В заморозке 🥶 - {users_data[1]}\n\n'
                 f'Парней в Прогрессе - {users_data[2]}\n'
                 f'Девушек в Прогрессе - {users_data[3]}\n\n'
                 f'На 1️⃣ уровне - {users_data[4]}\n'
                 f'На 2️⃣ уровне - {users_data[5]}\n'
                 f'В Минкайфа 🐯🦁  - {users_data[6]}\n'
                 f'В Старте 👨‍🚀 - {users_data[8]}\n'
                 f'На соревновательном 3️⃣ уровне - {users_data[7]}'
        )
        await message.answer(
            text='Введите первые буквы имени или фамилии атлета:'
        )


async def check_for_workouts_upload(message: types.Message, state: FSMContext):
    """
    Ckeck up for upload last week of workouts from google sheet with workouts.
    :param message: button value
    :param state: upload_workouts
    :return:
    """
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is None:
            pass
        else:
            await state.finish()
        logging.info('Cancelling state %r', current_state)
        await message.answer(
            'Перед загрузкой новой тренировочной недели в бота предлагаю'
            ' ещё раз проверить тренировки'
            'для исключения возможных ошибок в заданиях 🦕\n\n'
            ' Если все окей - "Да" \n\n'
            'Если после загрузки тренировок в бота нашлась ошибка,'
            ' то делаем следующие шаги:\n'
            '1. Удаляем неделю тренировок по кнопке "Удалить тренировки"\n'
            '2. Исправляем ошибки в гугл таблице\n'
            '3. Заново загружаем неделю тренировок',
            reply_markup=yes_or_no_inline_kb
        )
        await state.set_state(UsersInfo.upload_workouts)


async def check_for_workouts_delete(message: types.Message, state: FSMContext):
    """

    :param message:
    :param state:
    :return:
    """
    if message.from_user.id in ADMIN_IDS:
        current_state = await state.get_state()
        if current_state is None:
            pass
        else:
            await state.finish()
        logging.info('Cancelling state %r', current_state)
        await message.answer(
            'При согласии для всех основных уровней, будет удалена последняя'
            'неделя тренировок.\n\nКак только ошибка будет исправлена в нужном'
            'месте, смело загружай новую неделю заново!',
            reply_markup=yes_or_no_inline_kb)
        await state.set_state(UsersInfo.delete_workouts)


async def upload_last_week_workouts(query: types.CallbackQuery,
                                    state: FSMContext):
    """
	Загружает последнюю неделю тренировок в базу данных.
    :param query:
    :param state:
    :return:
    """
    if query.data == 'yes_action':
        await get_data_from_google_sheet(SHEET_TITLE, JSON_PATH)
        await query.message.answer('Тренировки загружены для всех уровней')
        await query.answer()
    if query.data == 'no_action':
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await query.message.answer('Отменил', reply_markup=admin_tools)
        await query.answer()


async def delete_last_week_workouts(query: types.CallbackQuery,
                                    state: FSMContext):
    """
    Удалеяет последнюю неделю тренировок из базы данных.
    :param query:
    :param state:
    :return:
    """
    if query.data == 'yes_action':
        await delete_workouts_from_database(SHEET_TITLE, JSON_PATH)
        await query.message.answer('Тренировки последней недели удалены')
        await query.answer()
    if query.data == 'no_action':
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await query.message.answer('Отменил', reply_markup=admin_tools)
        await query.answer()


async def message_to_all_via_bot(message: types.Message, state: FSMContext):
    """
    Choosing option to send message to all via bot.
    :param message:
    :param state:
    :return:
    """
    if message.from_user.id in ADMIN_IDS:
        await state.set_state(UsersInfo.send_to_all_via_bot)
        await message.answer(
            text='Введи сообщение, которое хочешь отправить всем'
        )


async def approve_sending_message_to_all(message: types.Message,
                                         state: FSMContext):
    """
    Getting text from users text message and poping inline keyboard with
    yes or no action to approve sending the message.
    :param message:
    :param state:
    :return:
    """
    if message.from_user.id in ADMIN_IDS:
        async with state.proxy() as info:
            info['message_to_all'] = message.text
        await message.answer(
            text='Ты хочешь отправить сообщение?',
            reply_markup=yes_or_no_inline_kb
        )
        await state.set_state(UsersInfo.approval)


async def send_message_to_all_via_bot(query: types.CallbackQuery,
                                      state: FSMContext):
    """
    If answer is yes sending message to all users with active subscription.
    If no goes back to enter
    :param query:
    :param state:
    :return:
    """
    async with state.proxy() as info:
        message_text = info['message_to_all']
        if query.data == 'yes_action':
            users_id = await db.get_users_id_with_sub()
            for user_data in users_id:
                try:
                    await bot.send_message(
                        text=message_text,
                        chat_id=user_data[0]
                    )
                except ChatNotFound:
                    logging.info('Нету чата с этим пользователем')
            await query.message.answer('Готово')
            await state.finish()
        elif query.data == 'no_action':
            await state.set_state(UsersInfo.send_to_all_via_bot)
            await query.message.answer(
                text='Введи новое сообщение, которое хочешь отправить всем'
            )
    await query.answer()


async def get_list_of_users(message: types.Message,
                            state: FSMContext) -> None:
    """
    Get list of users by search phrase from admin.
    :param message: message.text - search phrase
    :param state:
    :return:
    """
    users_info = await db.get_user_info(message.text)
    async with state.proxy() as data:
        data['chosen_users'] = message.text
    await db.update_chosen_users(state, message.from_user.id)
    await message.answer(
        'Вот кого удалось найти:',
        reply_markup=await users_info_inline_kb(users_info)
    )
    await state.set_state(UsersInfo.user_management)


async def get_list_of_inactive_users(message: types.Message,
                                     state: FSMContext) -> None:
    """
    Get list of inline buttons with inactive users for admin.
    """
    await message.answer(
        'Список неактивных пользователей:',
        reply_markup=await users_info_inline_kb(
            await db.get_inactive_users_info()
        )
    )
    await state.set_state(UsersInfo.inactive_user_managment)


async def inactive_user_management(query: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """
    After selecting inactive user pops up management menu.
    """
    users_by_telegram_id = await users_management(
        await db.get_inactive_users_info()
    )
    if int(query.data) in list(users_by_telegram_id.keys()):
        user_data_by_id = users_by_telegram_id.get(int(query.data))[0]
        async with state.proxy() as data:
            data['user_id'] = int(query.data)
            data['nickname'] = user_data_by_id[4]
            data['first_name'] = user_data_by_id[0]
            data['last_name'] = user_data_by_id[1]
        await state.set_state(UsersInfo.actions_on_user)
        await bot.edit_message_text(
            text=f'Вы выбрали:\n@{user_data_by_id[4]}\n'
                 f'{user_data_by_id[0]} {user_data_by_id[1]}\n'
                 f'Уровень - {user_data_by_id[2]}\n'
                 f'В прогрессе с {user_data_by_id[5]}\n\n'
                 f'Действия:',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=user_action_inline_kb
        )
        await query.answer()


async def user_management_menu(query: types.CallbackQuery,
                               state: FSMContext) -> None:
    """
    After selecting a user pops up a management menu.
    :param query:
    :param state:
    :return:
    """
    users_by_telegram_id = await users_management(
        await db.get_chosen_users(query.from_user.id)
    )
    if int(query.data) in list(users_by_telegram_id.keys()):
        user_data_by_id = users_by_telegram_id.get(int(query.data))[0]
        async with state.proxy() as data:
            data['user_id'] = int(query.data)
            data['nickname'] = user_data_by_id[4]
            data['first_name'] = user_data_by_id[0]
            data['last_name'] = user_data_by_id[1]
        await state.set_state(UsersInfo.actions_on_user)
        await bot.edit_message_text(
            text=f'Вы выбрали:\n@{user_data_by_id[4]}\n'
            f'{user_data_by_id[0]} {user_data_by_id[1]}\n'
            f'Уровень - {user_data_by_id[2]}\n'
            f'В прогрессе с {user_data_by_id[5]}\n\n'
            f'Действия:',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=user_action_inline_kb
        )
        await query.answer()


async def add_new_user(message: types.Message,
                       state: FSMContext) -> None:
    """
    Asks a telegram_id for new user to add manually.
    """
    await message.answer(
        f'Введи telegram_id нового пользователя\n\n'
        f'Свой telegram_id новый пользователь может узнать у @userinfobot'
    )
    await state.set_state(UsersInfo.add_new_user)


async def insert_new_user_into_database(message: types.Message,
                                        state: FSMContext) -> None:
    """
    Gets telegram_id and adds new user ti database with 30 days subs active.
    """
    telegram_id = int(message.text)
    if not await db.user_payed_not_registered(telegram_id):
        registration_date = datetime.now().date()
        subscription_till = (datetime.now() + timedelta(days=30)).date()
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['registration_date'] = registration_date
            data['subscribtion_date'] = subscription_till
            data['sub_status'] = True
            data['freeze_status'] = False
        await db.add_user_manually_by_admin(state)
        await message.answer(
            f'Пользователь с telegram_id: {data["telegram_id"]} добавлен в бота.\n'
            f'Дата регистрации сегодня \n'
            f'Подписка до {subscription_till.strftime("%d.%m.%Y")}\n\n'
            f'Новому пользователю необходимо закончить регистрацию в боте'
        )
        await state.finish()
    else:
        await message.answer(
            f'Пользователь с telegram_id: {telegram_id} уже есть в боте!'
        )
        await state.finish()


async def actions_under_user(query: types.CallbackQuery,
                             state: FSMContext) -> None:
    """
    Actions on inline keyboard from inline keyboard with chosen user by admin.
    :param query:
    :param state:
    :return:
    """
    async with state.proxy() as data:
        if query.data == 'change_level_of_user':
            await state.set_state(UsersInfo.change_level)
            await bot.edit_message_text(
                text=f'Выберите уровень для пользователя @{data["nickname"]}\n'
                     f'{data["first_name"]} {data["last_name"]}',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id,
                reply_markup=choose_kb
            )
            await query.answer()
        elif query.data == 'cancel_subscription':
            await state.set_state(UsersInfo.cancel_subscription)
            await bot.edit_message_text(
                text=f'Вы хотите отменить подписку '
                     f'для  {data["first_name"]} {data["last_name"]}?',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id,
                reply_markup=yes_or_no_inline_kb
            )
        elif query.data == 'add_subscription':
            await state.set_state(UsersInfo.add_subscription)
            await bot.edit_message_text(
                text=f'Сколько дней добавить '
                     f'в подписку для @{data["nickname"]}\n'
                     f'{data["first_name"]} {data["last_name"]}? ',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id
            )
        elif query.data == 'send_message_via_bot':
            await state.set_state(UsersInfo.send_message_via_bot)
            await bot.edit_message_text(
                text=f'Напиши текст сообщения, которое будет отправлено '
                     f'через меня 🤖 для @{data["nickname"]}\n'
                     f'{data["first_name"]} {data["last_name"]}',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id
            )
        elif query.data == 'freeze_subscription':
            await state.set_state(UsersInfo.freeze_subscription)
            await bot.edit_message_text(
                text=f'Укажи количество дней заморозки для @{data["nickname"]} '
                     f'{data["first_name"]} {data["last_name"]}',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id
            )
        elif query.data == 'weekly_dynamic':
            await user_weekly_dynamic_graph(telegram_id=data['user_id'])
            await bot.send_photo(
                chat_id=query.message.chat.id,
                photo=open(f'media/{data["user_id"]}_weekly.png', 'rb'),
                caption='Еженедельная динамика для выбранного пользователя'
            )
            os.remove(f'media/{data["user_id"]}_weekly.png')
            await query.answer()

async def change_level_of_user(query: types.CallbackQuery, state: FSMContext):
    """
    Changes user level by admin via inline keyboard.
    :param query:
    :param state:
    :return:
    """
    if query.data == 'start_level':
        user_level = 'Старт'
    elif query.data == 'first_level':
        user_level = 'Первый'
    elif query.data == 'second_level':
        user_level = 'Второй'
    elif query.data == 'competition_level':
        user_level = 'Соревнования'
    elif query.data == 'minkaif_level':
        user_level = 'Минкайфа'
    async with state.proxy() as info:
        info['new_level'] = user_level
    await db.update_user_level(state)
    await bot.send_message(chat_id=info['user_id'],
                           text=f'Твой уровень изменён на '
                                f'{user_level}!\n\n'
                                f'Прогрессивных тренировок 💪')
    await bot.edit_message_text(
        text=f'Уровень для @{info["nickname"]} изменён на {user_level}',
        message_id=query.message.message_id,
        chat_id=query.message.chat.id,
    )
    await state.finish()
    await query.answer()


async def cancel_user_subscription(query: types.CallbackQuery,
                                   state: FSMContext) -> None:
    """
    Cancel user susbscirption via admin desicion. Just makes a sub date
    a minus week from today day.
    :param query:
    :param state:
    :return:
    """
    async with state.proxy() as info:
        if query.data == 'yes_action':
            await db.cancel_user_subscription(telegram_id=info['user_id'])
            await db.deactivate_subscription_status(telegram_id=info['user_id'])
            try:
                await bot.send_message(
                    chat_id=info['user_id'],
                    text='Твоя подписка была отменена! Для подробностей - '
                         'напиши @fserkov'
                )
            except ChatNotFound:
                logging.info('Чат не найден!')
            await bot.edit_message_text(
                text=f'Подписка @{info["nickname"]} отменена!',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id,
            )
            await state.finish()
            await query.answer()
        elif query.data == 'no_action':
            current_state = await state.get_state()
            if current_state is None:
                return
            logging.info('Cancelling state %r', current_state)
            await state.finish()
            await query.message.answer('Отменил', reply_markup=admin_tools)
            await query.answer()


async def add_subscription_to_user(message: types.Message,
                                   state: FSMContext):
    """
    Adds subscription to user without money by admin.
    :param message:
    :param state:
    :return:
    """
    async with state.proxy() as info:
        await db.add_user_subscription(
            telegram_id=info['user_id'],
            days=message.text
        )
        await db.activate_subscription_status(telegram_id=info['user_id'])
        new_sub_date = await db.get_user_subscription_date(info['user_id'])
        await message.answer(
            f'Подписка для @{info["nickname"]} продлена до {new_sub_date}'
        )
        await bot.send_message(
            chat_id=info['user_id'],
            text=f'Тебе продлили подписку до {new_sub_date}'
        )
    await state.finish()


async def send_message_to_user_via_bot(message: types.Message,
                                       state: FSMContext):
    """
    Sends message to user via bot.
    :param message:
    :param state:
    :return:
    """
    text_for_user = message.text
    try:
        async with state.proxy() as info:
            await bot.send_message(
                chat_id=info['user_id'],
                text=text_for_user
            )
            await message.answer(
                f'Cообщение пользователю @{info["nickname"]} отправлено!'
            )
        await state.finish()
    except ValueError:
        logging.info('Такого пользователя нету', info['user_id'])


async def get_any_workout_for_admin(
        query: types.CallbackQuery,
        state: FSMContext
) -> None:
    """
    Send a message via bot to the admin with the workout of any level
    for chosen date.
    :param query:
    :return:
    """
    levels_from_database = {
        'first_level': 'Первый',
        'second_level': 'Второй',
        'competition_level': 'Соревнования',
        'minkaif_level': 'Минкайфа',
    }
    admin_answer = levels_from_database.get(query.data)
    telegram_id = query.from_user.id
    chosen_date = await db.get_chosen_date(telegram_id)
    chosen_date = datetime.strptime(
        chosen_date, '%Y-%m-%d').date()
    workout = await db.get_any_level_workout_for_admin(
        chosen_date, admin_answer
    )
    await query.message.edit_text(
        text=f'Уровень: {levels_from_database.get(query.data)}\n\n' + workout)
    await state.finish()
    await query.answer()


def register_admin_handlers(dp: Dispatcher):
    """
    Registration of admin handlers
    """
    dp.register_callback_query_handler(actions_under_user,
                                       lambda query: True,
                                       state=UsersInfo.actions_on_user)
    dp.register_callback_query_handler(change_level_of_user,
                                       lambda query: True,
                                       state=UsersInfo.change_level)
    dp.register_callback_query_handler(cancel_user_subscription,
                                       lambda query: True,
                                       state=UsersInfo.cancel_subscription)
    dp.register_callback_query_handler(user_management_menu,
                                       lambda query: True,
                                       state=UsersInfo.user_management)
    dp.register_callback_query_handler(inactive_user_management,
                                       lambda query: True,
                                       state=UsersInfo.inactive_user_managment)
    dp.register_callback_query_handler(send_message_to_all_via_bot,
                                       lambda query: True,
                                       state=UsersInfo.approval)
    dp.register_callback_query_handler(upload_last_week_workouts,
                                       lambda query: True,
                                       state=UsersInfo.upload_workouts)
    dp.register_callback_query_handler(delete_last_week_workouts,
                                       lambda query: True,
                                       state=UsersInfo.delete_workouts)
    dp.register_callback_query_handler(get_any_workout_for_admin,
                                       lambda query: True,
                                       state=ChosenDateData.for_admin)
    dp.register_message_handler(send_message_to_user_via_bot,
                                state=UsersInfo.send_message_via_bot)
    dp.register_message_handler(add_subscription_to_user,
                                state=UsersInfo.add_subscription)
    dp.register_message_handler(show_administration_tools,
                                text='🧙 Aдминка',
                                state='*')
    dp.register_message_handler(find_users_by_names,
                                text='👫 Операции с атлетами',
                                state='*')
    dp.register_message_handler(add_new_user,
                                text='👤 Добавить нового пользователя',
                                state='*')
    dp.register_message_handler(insert_new_user_into_database,
                                state=UsersInfo.add_new_user)
    dp.register_message_handler(get_list_of_inactive_users,
                                text='👥 Неактивные пользователи',
                                state='*')
    dp.register_message_handler(check_for_workouts_upload,
                                text='⏬ Добавить новые тренировки',
                                state='*')
    dp.register_message_handler(check_for_workouts_delete,
                                text='⚠️ Удалить последнюю неделю тренировок',
                                state='*')
    dp.register_message_handler(message_to_all_via_bot,
                                text='📢 Сообщение всем',
                                state='*')
    dp.register_message_handler(approve_sending_message_to_all,
                                state=UsersInfo.send_to_all_via_bot)
    dp.register_message_handler(get_list_of_users,
                                state=UsersInfo.find_users)
    dp.register_message_handler(back_to_main_menu, text='⏪ Главное меню',
                                state="*")
