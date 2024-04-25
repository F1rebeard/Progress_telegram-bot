import logging
import sqlite3 as sql
import numpy as np

from datetime import datetime, timedelta, date
from aiogram.dispatcher import FSMContext


class Database:
    def __init__(self, db_file):
        self.connection = sql.connect(db_file)
        self.cursor = self.connection.cursor()
        print('Database is online!')

    # NEW USER REGISTRATION
    async def add_user(self, state: FSMContext) -> None:
        """
        Adds telegram_id and user telegram nickname after payment.
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO users("
                    "telegram_id, username, registration_date"
                    ") "
                    " VALUES (?, ?, ?)", tuple(data.values())
                )

    async def add_user_manually_by_admin(self, state: FSMContext) -> None:
        """
        Adds new user into database after payment via website.
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO users("
                    "telegram_id, registration_date, subscribtion_date, "
                    "sub_status, freeze_status) "
                    "VALUES  (?, ?, ?, ?, ?)", tuple(data.values())
                )

    async def user_final_registration(
            self, state: FSMContext, telegram_id: int) -> None:
        """
        Full registration of user.
        :param state:
        :return:
        """
        try:
            async with state.proxy() as data:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users SET "
                        "first_name = ?, last_name = ?, gender = ?, email = ?,"
                        " level = ?, chosen_date = ? "
                        "WHERE telegram_id = ?", (
                            data['first_name'], data['last_name'],
                            data['gender'], data['email'], data['level'],
                            data['chosen_date'], telegram_id
                        )
                    )
        except ValueError or TypeError:
            logging.info('Пользователь не найден', telegram_id)

    async def user_start_final_registration(
            self, state: FSMContext, telegram_id: int) -> None:
        """
        Full registration of user.
        :param state:
        :return:
        """
        try:
            async with state.proxy() as data:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users SET "
                        "first_name = ?, last_name = ?, gender = ?, email = ?,"
                        " chosen_date = ? "
                        "WHERE telegram_id = ?", (
                            data['first_name'], data['last_name'],
                            data['gender'], data['email'],
                            data['chosen_date'], telegram_id
                        )
                    )
        except ValueError or TypeError:
            logging.info('Пользователь не найден', telegram_id)

    async def user_exists(self, telegram_id: int) -> bool:
        """
        Check user by his telegram_id if he exists in database.
        """
        try:
            with self.connection:
                user_info = self.cursor.execute(
                    "SELECT "
                    "first_name, last_name, email, level, gender "
                    "FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchall()
            result = []
            if bool(len(user_info)):
                for data in user_info[0]:
                    if data is not None:
                        result.append(data)
            return bool(len(result))
        except ValueError or TypeError:
            logging.info('Пользователь не найден', telegram_id)

    async def user_payed_not_registered(self, telegram_id):
        """
        Check if user paid but didn't register.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                user_info = self.cursor.execute(
                    "SELECT telegram_id, registration_date "
                    "FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchall()
            return bool(len(user_info))
        except ValueError or TypeError:
            logging.info('Пользователь не найдет', telegram_id)

    # УПРАВЛЕНИЕ ПОДПИСКОЙ ПОЛЬЗОВАТЕЛЕЙ И СТАТУС ПОДПИСКИ
    async def activate_subscription_status(self, telegram_id: int):
        """
        Adds True to sub status for user by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET sub_status = True "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def deactivate_subscription_status(self, telegram_id: int):
        """
        Adds False to sub status for user by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET sub_status = False "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def activate_freeze_status(self, telegram_id: int):
        """
        Adds True to freeze_status for selected  user via telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET freeze_status = True "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def deactivate_freeze_status(self, telegram_id: int):
        """
        Adds False to freeze_status for selected user via telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET freeze_status = False "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def clear_frozen_till_data(self, telegram_id: int):
        """
        Clear frozen_till data from cell for user via telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET frozen_till = NULL "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except ValueError:
            logging.info('Такого пользователя не существует', telegram_id)

    async def check_subscription_status(self, telegram_id: int):
        """
        Checks sub_status for user by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                sub_status = self.cursor.execute(
                    "SELECT sub_status "
                    "FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchone()
            return sub_status[0]
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def check_freeze_status(self, telegram_id: int):
        """
        Check freeze_status four user by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                freeze_status = self.cursor.execute(
                    "SELECT freeze_status "
                    "FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchone()
            return freeze_status[0]
        except ValueError:
            return f'Пользователя с {telegram_id} не существует в базе!'

    async def get_user_frozen_till_date(self,
                                        telegram_id: int) -> datetime.date:
        """
        Check frozen_till date for user by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                frozen_till = self.cursor.execute(
                    "SELECT frozen_till "
                    "FROM users "
                    "WHERE telegram_id =?", (telegram_id,)
                ).fetchone()
            return datetime.strptime(frozen_till[0], "%Y-%m-%d").date()
        except TypeError or ValueError:
            logging.info('Нет данных о заморозке', telegram_id)

    async def get_users_frozen_till_dates(self) -> [tuple, str]:
        """
        Gets tuple with telegram id and freeze date
        :return:
        """
        try:
            with self.connection:
                frozen_users = self.cursor.execute(
                    "SELECT telegram_id, frozen_till "
                    "FROM users "
                    "WHERE frozen_till IS NOT NULL"
                ).fetchall()
                return frozen_users
        except ValueError or TypeError:
            logging.info('Нету данных о заморозке', frozen_users)

    async def get_users_subscription_date(self) -> [tuple, str]:
        """
        Get users last day of subscription.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                subscribe_till = self.cursor.execute(
                    "SELECT telegram_id, subscribtion_date "
                    "FROM users "
                ).fetchall()
                return subscribe_till
        except ValueError or TypeError:
            return 'Нету данных о подписке!'

    async def get_user_subscription_date(self,
                                         telegram_id: int) -> datetime.date:
        """
        Get user subs date by telegram_id.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                subs_date = self.cursor.execute(
                    "SELECT subscribtion_date"
                    " FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchone()
            return datetime.strptime(subs_date[0], "%Y-%m-%d").date()
        except TypeError or ValueError:
            logging.info('Нет данных о подписке', telegram_id)

    async def update_user_subscription(self, telegram_id: int):
        """
        Adds new 30 days to user subscription with payment by user.
        :param telegram_id:
        :return:
        """
        try:
            sub_date = await self.get_user_subscription_date(telegram_id)
            today = datetime.now().date()
            if sub_date > today:
                initial_date = sub_date
            else:
                initial_date = today
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = date( ? , '+30 days') "
                    "WHERE telegram_id = ?", (initial_date, telegram_id)
                )
        except TypeError or ValueError:
            return 'Пользователь не найден'

    async def cancel_user_subscription(self, telegram_id: int):
        """
        Cancels user_subs by making sub date to minus week from today.
        :param telegram_id:users
        :return:
        """
        try:
            sub_date = await self.get_user_subscription_date(telegram_id)
            today = datetime.now().date()
            if sub_date >= today:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users "
                        "SET subscribtion_date =  date(?, '-1 day') "
                        "WHERE telegram_id = ?", (today, telegram_id)
                    )
        except TypeError or ValueError:
            logging.info('Пользователь не найден', telegram_id)

    async def add_user_subscription(self, telegram_id: int, days: str):
        """
        Add days to user subscription by admin.
        :param telegram_id:
        :return:
        """
        try:
            sub_date = await self.get_user_subscription_date(telegram_id)
            new_sub_date = sub_date + timedelta(days=int(days))
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = ? "
                    "WHERE telegram_id = ?", (new_sub_date, telegram_id)
                )
        except TypeError or ValueError:
            logging.info('Пользователь не найден!', telegram_id)

    async def decrease_user_subscription(self, telegram_id: int):
        """
        Decrease user subs day after canceling freeze_status.
        :param telegram_id:
        :return:
        """
        try:
            sub_date = await self.get_user_subscription_date(telegram_id)
            frozen_till = await self.get_user_frozen_till_date(telegram_id)
            today = datetime.now().date()
            days_diff = (frozen_till - today).days
            new_sub_date = sub_date - timedelta(days=int(days_diff))
            print(sub_date)
            print(today)
            print(days_diff)
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = ? "
                    "WHERE telegram_id = ?", (new_sub_date, telegram_id)
                )
        except TypeError or ValueError:
            logging.info('Пользователь не найден!', telegram_id)

    async def freeze_user_subscription(self, telegram_id: int,
                                       freeze_days: int):
        """
        Freezes user sub on freeze_days amount
        :param telegram_id:
        :param freeze_days:
        :return:
        """
        try:
            today = datetime.now().date()
            freeze_till = today + timedelta(days=freeze_days)
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET frozen_till = ?"
                    "WHERE telegram_id = ?", (freeze_till, telegram_id)
                )
        except TypeError or ValueError:
            logging.info('Пользователь не найден', telegram_id)

    async def new_user_subscription(self, telegram_id: int):
        """
        Adds 30 days from today's date to new user.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = date("
                    "registration_date , '+30 days') "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except TypeError or ValueError:
            return 'Пользователь не найден'

    async def add_one_month_for_start_new_user(self, telegram_id: int):
        """
        Adds 40 days from today's date to new user for start programm.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = date("
                    "registration_date , '+40 days') "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except TypeError or ValueError:
            return 'Пользователь не найден'

    async def add_full_start_for_user(self, telegram_id: int):
        """
        Adds 105 days for full 'Start' programm for new user.
        :param telegram_id:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET subscribtion_date = date("
                    "registration_date , '+105 days') "
                    "WHERE telegram_id = ?", (telegram_id,)
                )
        except TypeError or ValueError:
            return 'Пользователь не найден'



    # ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЯХ
    async def get_users_id_with_sub(self):
        """
        Get all users telegram_ids with subsbscription is up-to-date.
        :return:
        """
        try:
            today = datetime.now().date()
            with self.connection:
                users_id = self.cursor.execute(
                    "SELECT telegram_id "
                    "FROM users "
                    "WHERE subscribtion_date >= ?", (today,)
                ).fetchall()
            return users_id
        except ValueError or TypeError:
            logging.info('Что-то с датой', today)

    async def get_user_biometrics(self, telegram_id: int) -> tuple:
        """
        Get biometric profile data for user from users table
        :param telegram_id:
        :return:
        """
        with self.connection:
            biometrics = self.cursor.execute(
                f" SELECT level, gender, height, weight, birthdate"
                f" FROM users WHERE telegram_id = ?", (telegram_id,)).fetchone()
            return biometrics

    async def get_user_name(self, telegram_id: int) -> tuple:
        """
        Get name and surname of user for graph tittle and level
        :param telegram_id:
        :return:
        """
        with self.connection:
            data = self.cursor.execute(
                f" SELECT first_name, last_name, level"
                f" FROM users WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
            return data

    # УПРАВЛЕНИЕ И КОНТРОЛЬ УРОВНЕЙ АТЛЕТОВ
    async def get_user_level(self, telegram_id: int) -> [list, str]:
        """
        Get user level from users table and returns it
        :param telegram_id: id provided by message from user
        :return user_level:  a list, with the user level
        """
        try:
            with self.connection:
                user_level = self.cursor.execute(
                    "SELECT level FROM users "
                    "WHERE telegram_id = ?", (int(telegram_id),)
                ).fetchone()
                return user_level[0]
        except TypeError:
            return f'Пользователь не найден.'

    async def get_users_data(self) -> [list, str]:
        """
        Get lists of users with gender, sub_status, freeze_status and level.
        :return:
        """
        try:
            with self.connection:
                users_data = self.cursor.execute(
                    "SELECT gender, level, sub_status, freeze_status "
                    "FROM users "
                    "WHERE sub_status IS TRUE"
                ).fetchall()
            return users_data
        except ValueError or TypeError:
            logging.info('Нет данных!')

    async def update_user_level(self, state: FSMContext) -> None:
        try:
            async with state.proxy() as data:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users SET level = ?"
                        "WHERE telegram_id = ?", (data['new_level'],
                                                  data['user_id'])
                    )
        except TypeError or ValueError:
            return logging.info('Пользователь не найден', data['user_id'])

    async def add_start_level_to_new_user(self, state: FSMContext) -> None:
        try:
            async with state.proxy() as data:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users SET level = 'Старт' "
                        "WHERE telegram_id = ?",(data['telegram_id'],)
                    )
        except TypeError or ValueError:
            return logging.info('Пользователь не найден!')

    async def get_registration_date(self, telegram_id: int):
        """
        Get's registration date for user.
        """
        try:
            with self.connection:
                reg_date = self.cursor.execute(
                    "SELECT registration_date "
                    "FROM users "
                    "WHERE telegram_id = ?", (telegram_id,)
                ).fetchone()
            return datetime.strptime(reg_date[0], "%Y-%m-%d").date()
        except TypeError or ValueError:
            return logging.info('Пользователь не найден!')

    # КАЛЕНДАРЬ ТРЕНИРОВОК
    async def get_workout_for_user(
            self, date: datetime, telegram_id: int) -> str:
        """
        Get workout by chosen date and level of user.
        :param telegram_id: user telegram id
        :param date: date of selected workout
        :return: str the workout for selected date
        """
        user_level = await self.get_user_level(telegram_id)
        # inserting the workout table name into database
        try:
            with self.connection:
                workout = self.cursor.execute(
                    f"SELECT workout "
                    f"FROM workouts "
                    f"WHERE date = ? AND level = ?", (date, user_level)
                ).fetchone()
                if workout is None:
                    return f'В этот день нет тренировки!'
                else:
                    return f'{workout[0]}'
        except ValueError or TypeError:
            logging.info('Нет такой тренировки!')

    async def get_any_level_workout_for_admin(
            self, date: datetime, level: str) -> str:
        """
        Gets the workout of selected level for admin.
        :param date: chosen date from users.chosen_date
        :param level: selected via inline_keyboard by admin
        :return:
        """
        try:
            with self.connection:
                workout = self.cursor.execute(
                    f'SELECT workout '
                    f'FROM workouts '
                    f'WHERE date = ? AND level = ?',(date, level)
                ).fetchone()
                if workout is None:
                    return f'В этот день нет тренировки!'
                else:
                    return f'{workout[0]}'
        except ValueError or TypeError:
            logging.info('Нет такой тренировки!')

    async def get_start_workout_for_user(self, workout_day: int) -> str:
        """
        Get workout text for chosen day from start workouts for user.
        """
        try:
            with self.connection:
                workout = self.cursor.execute(
                    'SELECT workout_text '
                    'FROM start_workouts '
                    'WHERE workout_day = ?', (workout_day,)
                ).fetchone()
            if workout is None:
                return f'В этот день нет тренировки!'
            else:
                return f'{workout[0]}'
        except ValueError or TypeError:
            logging.info('Нет такой тренировки!')

    async def workout_dates_chosen_date(self, telegram_id: int) -> list:
        """
        get list of workout dates in datetime.datetime format
        :param telegram_id: telegram id of user
        :return: list
        """
        user_level = await self.get_user_level(telegram_id)
        user_subscription = await self.get_user_subscription_date(telegram_id)
        two_weeks_before = (datetime.now() - timedelta(weeks=2)).date()
        result = []
        with self.connection:
            data_list = self.cursor.execute(
                f"SELECT date FROM workouts WHERE level = ?", (user_level,)
            ).fetchall()
        for date_tuple in data_list:
            for str_date in date_tuple:
                date = datetime.strptime(str_date, '%Y-%m-%d').date()
                if two_weeks_before <= date <= user_subscription:
                    result.append(date)
        return result

    async def workout_dates_for_admin(self, telegram_id: int) -> list:
        """
        Gets list of workout for all level for admin in datetime.datetime form.
        """
        admin_subscription = await self.get_user_subscription_date(telegram_id)
        four_weeks_before = (datetime.now() - timedelta(weeks=4)).date()
        result = []
        with self.connection:
            dates = self.cursor.execute(
                f"SELECT date "
                f"FROM workouts "
                f"WHERE level IN ('Первый', 'Минкайфа')"
            ).fetchall()
        for date_tuple in dates:
            for str_date in date_tuple:
                date = datetime.strptime(str_date, '%Y-%m-%d').date()
                if four_weeks_before <= date <= admin_subscription:
                    result.append(date)
        return result

    async def get_days_of_start(self, days_to_show: int) -> list:
        """
        Get list of workout_days from start_workout table for calendar.
        """
        with self.connection:
            workout_days = self.cursor.execute(
                "SELECT workout_day FROM start_workouts "
                "WHERE workout_day <= ?", (days_to_show,)
            ).fetchall()
            return workout_days

    async def collect_workout_dates(self, telegram_id: int) -> list:
        """
        List of workout dates for level of user for workout calendar.
        :param telegram_id:
        :return: list
        """
        user_level = await self.get_user_level(telegram_id)
        workouts_dates = []
        with self.connection:
            data = self.cursor.execute(
                f"SELECT date FROM workouts "
                f"WHERE level = ?", (user_level,)
            ).fetchall()
            for date in data:
                workouts_dates.append(date[0])
        return workouts_dates

    async def update_chosen_date(
            self, telegram_id: int, date: datetime) -> None:
        """
        Update chosen_date column in users table for user
        with chosen telegram_id.
        :param telegram_id:
        :param date:
        :return:
        """
        with self.connection:
            self.cursor.execute(
                "UPDATE users SET chosen_date = ?"
                "WHERE telegram_id = ?", (date, telegram_id)
            )

    async def get_chosen_date(self, telegram_id: int) -> datetime:
        """
        Returns the date from chosen_date column from user table for user with
        selected telegram_id.
        :param telegram_id:
        :return:
        """
        with self.connection:
            chosen_date = self.cursor.execute(
                f" SELECT chosen_date"
                f" FROM users WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
            return chosen_date[0]

    async def upload_new_workouts(self, workouts: list):
        """
        get the row with new workouts from google table and inserts it into
        a database into workouts table.
        :param workouts:
        :return:
        """
        try:
            sql = (
                "INSERT INTO workouts(date, workout, level) "
                "VALUES (?, ?, ?)"
            )
            with self.connection:
                self.cursor.execute(sql, tuple(workouts))
        except ValueError:
            return 'Нету данных'

    async def delete_last_workouts(self, dates: list):
        """
        Delete workouts for all levels with dates from dates list.
        :param dates:
        :return:
        """
        try:
            sql = (
                "DELETE FROM workouts "
                "WHERE date = ?"
            )
            with self.connection:
                for date in dates:
                    self.cursor.execute(sql, (date,))
        except ValueError:
            return 'Нету данных'

    # ДАННЫЕ ПО ПРОФИЛЮ ПОЛЬЗОВАТЕЛЯ
    # ПОСЛЕДНИЕ ДАННЫЕ МАКСИМАЛЬНЫХ ЗНАЧЕНИЙ ДЛЯ ОТОБРАЖЕНИЯ В РАЗДЕЛАХ ПРОФИЛЯ
    async def get_user_last_strength_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get strength data for user by telegram_id for inline buttons
         in strength category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                strength_buttons = self.cursor.execute(
                    f"SELECT movement, MAX(date), result "
                    f"FROM strength WHERE telegram_id = ? "
                    f"GROUP BY movement", (telegram_id,)
                ).fetchall()
                return strength_buttons
        except ValueError:
            return f"Нету данных!"

    async def get_user_last_power_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get explosive power data for user by telegram_id for inline buttons
        in explosive power category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                power_buttons = self.cursor.execute(
                    f"SELECT movement, MAX(date), result "
                    f"FROM explosive_power WHERE telegram_id = ? "
                    f"GROUP BY movement", (telegram_id,)
                ).fetchall()
                return power_buttons
        except ValueError:
            return f"Нету данных!"

    async def get_user_last_strength_capacity_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get strength capacity reps for user by telegram_id for inline buttons
        in strength capacity category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                reps_for_buttons = self.cursor.execute(
                    f"SELECT movement, MAX(date), result_reps, result_weight "
                    f"FROM strength_capacity WHERE telegram_id = ? "
                    f"GROUP BY movement", (telegram_id,)
                ).fetchall()
                return reps_for_buttons
        except ValueError:
            return f"Нету данных!"

    async def get_user_last_aerobic_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get aerobic capacity results for user by telegram_id for inline buttons
        in aerobic capacity category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                aerobic_buttons = self.cursor.execute(
                    f'SELECT movement, MAX(date), result, time_result '
                    f'FROM aerobic_capacity WHERE telegram_id = ? '
                    f'GROUP BY  movement', (telegram_id,)
                ).fetchall()
                return aerobic_buttons
        except ValueError:
            return 'Нету данных!'

    async def get_user_metcons_last_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get metcons results for user by telegram_id for inline buttons in
        metcons category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                metcons_buttons = self.cursor.execute(
                    f' SELECT metcon, MAX(date), result_reps, result_time'
                    f' FROM metcons WHERE telegram_id = ?'
                    f' GROUP BY metcon', (telegram_id,)
                ).fetchall()
                return metcons_buttons
        except ValueError:
            return 'Нету данных!'

    async def get_user_last_gymnastics_result(
            self, telegram_id: int) -> [tuple, str]:
        """
        Get gymnastics results for user by telegram_id for inline buttons
        in gymnastics category.
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                aerobic_buttons = self.cursor.execute(
                    f'SELECT movement, MAX(date), result '
                    f'FROM gymnastics WHERE telegram_id = ? '
                    f'GROUP BY  movement', (telegram_id,)
                ).fetchall()
                return aerobic_buttons
        except ValueError:
            return 'Нету данных!'

    # ИСТОРИЯ РЕЗУЛЬТАТОВ
    async def strength_movement_result_history(
            self, telegram_id: int, movement: str) -> [tuple, str]:
        """
        Get strength records list for user by telegram_id and movement.
        :param telegram_id:
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_history = self.cursor.execute(
                    f"SELECT DATE(date), result "
                    f"FROM strength "
                    f"WHERE telegram_id = ? AND movement = ?"
                    f"ORDER BY date DESC;", (telegram_id, movement)
                ).fetchall()
                return movement_history
        except ValueError:
            return f"Нету данных!"

    async def power_movement_result_history(
            self, telegram_id: int, movement: str) -> [tuple, str]:
        """
        Get explosive power records list for user by telegram_id and movement.
        :param telegram_id:
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_history = self.cursor.execute(
                    f"SELECT DATE(date), result "
                    f"FROM explosive_power "
                    f"WHERE telegram_id = ? AND movement = ?"
                    f"ORDER BY date DESC;", (telegram_id, movement)
                ).fetchall()
                return movement_history
        except ValueError:
            return f"Нету данных!"

    async def strength_cpt_result_history(
            self, telegram_id: int, movement: str) -> [tuple, str]:
        """
        Get strength capacity records list for user by telegram_id and movement.
        :param telegram_id:
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_history = self.cursor.execute(
                    f"SELECT DATE(date), result_reps, result_weight "
                    f"FROM strength_capacity "
                    f"WHERE telegram_id = ? AND movement = ?"
                    f"ORDER BY date DESC;", (telegram_id, movement)
                ).fetchall()
                return movement_history
        except ValueError:
            return f'Нету данных!'

    async def aerobic_result_history(
            self, telegram_id: int, movement: str) -> [tuple, str]:
        """
        Get aerobic capacity movement history records for user by telegram_id
        and movement.
        :param telegram_id:
        :param movement:
        :return:
        """
        time_movements = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км']
        try:
            with self.connection:
                if movement in time_movements:
                    exercise_history = self.cursor.execute(
                        f"SELECT DATE(date), time_result "
                        f"FROM aerobic_capacity "
                        f"WHERE telegram_id = ? AND movement = ? "
                        f"ORDER BY date DESC;", (telegram_id, movement)
                    ).fetchall()
                else:
                    exercise_history = self.cursor.execute(
                        f"SELECT DATE(date), result "
                        f"FROM aerobic_capacity "
                        f"WHERE telegram_id = ? AND movement = ? "
                        f"ORDER BY date DESC;", (telegram_id, movement)
                    ).fetchall()
            return exercise_history
        except ValueError:
            return f'Нету данных!'

    async def metcon_result_history(
            self, telegram_id: int, metcon: str) -> [tuple, str]:
        """
        time_metcons = ['150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                    'Калсу', 'Open 19.5', 'Open 16.5']
        :param telegram_id:
        :param metcon:
        :return:
        """
        time_metcons = ['150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                        'Калсу', 'Open 19.5', 'Open 16.5']
        try:
            with self.connection:
                if metcon in time_metcons:
                    metcon_history = self.cursor.execute(
                        f"SELECT DATE(date), result_time "
                        f"FROM metcons "
                        f"WHERE telegram_id = ? AND metcon = ? "
                        f"ORDER BY date DESC;", (telegram_id, metcon)
                    ).fetchall()
                else:
                    metcon_history = self.cursor.execute(
                        f"SELECT DATE(date), result_reps "
                        f"FROM metcons "
                        f"WHERE telegram_id = ? AND metcon = ? "
                        f"ORDER BY date DESC;", (telegram_id, metcon)
                    ).fetchall()
            return metcon_history
        except ValueError:
            return f'Нету данных!'

    async def gymnastics_result_history(
            self, telegram_id: int, movement: str) -> [tuple, str]:
        """
        Get gymnastics movement history records for user by telegram_id
        and movement.
        :param telegram_id:
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_history = self.cursor.execute(
                    f"SELECT DATE(date), result "
                    f"FROM gymnastics "
                    f"WHERE telegram_id = ? AND movement = ?"
                    f"ORDER BY date DESC;", (telegram_id, movement)
                ).fetchall()
                return movement_history
        except ValueError:
            return f'Нету данных!'

    async def strength_movements_leaderboard(
            self, movement: str) -> [tuple, str]:
        """
        Get leaderboard for chosen strength movement by user.
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_leaderboard = self.cursor.execute(
                    f"SELECT users.username, users.first_name, users.last_name, "
                    f"users.level, leaderboard.result, leaderboard.latest_date "
                    f"FROM "
                    f"(SELECT telegram_id, movement, result, MAX(DATE(date)) "
                    f"AS latest_date FROM strength WHERE movement =? "
                    f"GROUP BY telegram_id ORDER BY result DESC) "
                    f"AS leaderboard JOIN users "
                    f"WHERE "
                    f"users.telegram_id = leaderboard.telegram_id", (movement,)
                ).fetchall()
            return movement_leaderboard
        except ValueError:
            return 'Нету данных!'

    # ЛИДЕРБОРДЫ
    async def power_movements_leaderboard(self, movement: str) -> [tuple, str]:
        """
        Get leaderboard for chosen explosive power movement by user.
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_leaderboard = self.cursor.execute(
                    f"SELECT "
                    f"users.username, users.first_name, users.last_name, "
                    f"users.level, leaderboard.result, leaderboard.latest_date "
                    f"FROM (SELECT telegram_id, movement, result, MAX(date) "
                    f"AS latest_date FROM explosive_power WHERE movement =? "
                    f"GROUP BY telegram_id ORDER BY result DESC) "
                    f"AS leaderboard JOIN users "
                    f"WHERE "
                    f"users.telegram_id = leaderboard.telegram_id", (movement,)
                ).fetchall()
            return movement_leaderboard
        except ValueError:
            return 'Нету данных!'

    async def strength_cpt_movements_leaderboard(
            self, movement: str) -> [tuple, str]:
        """
        Get leaderboard for chosen strength capacity movement by user.
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_leaderboard = self.cursor.execute(
                    f"SELECT "
                    f"users.username, users.first_name, users.last_name, "
                    f"users.level, leaderboard.koef_Sinkler, "
                    f"leaderboard.latest_date "
                    f"FROM "
                    f"(SELECT "
                    f"telegram_id, movement, koef_Sinkler, MAX(DATE(date)) "
                    f"AS latest_date FROM strength_capacity WHERE movement =? "
                    f"GROUP BY telegram_id ORDER BY koef_Sinkler DESC) "
                    f"AS leaderboard JOIN users "
                    f"WHERE "
                    f"users.telegram_id = leaderboard.telegram_id", (movement,)
                ).fetchall()
            return movement_leaderboard
        except ValueError:
            return 'Нету данных!'

    async def aerobic_movements_leaderboard(
            self, movement: str) -> [tuple, str]:
        """
        Get leaderboard for chosen aerobic capacity movement by user.
        :param movement:
        :return:
        """
        time_movements = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км']
        try:
            with self.connection:
                if movement in time_movements:
                    movement_leaderboard = self.cursor.execute(
                        "SELECT "
                        "users.username, users.first_name, users.last_name, "
                        "users.level, leaderboard.time_result, "
                        "leaderboard.latest_date "
                        "FROM "
                        "(SELECT "
                        "telegram_id, movement,"
                        " time_result, "
                        "MAX(DATE(date)) AS latest_date "
                        "FROM aerobic_capacity WHERE movement = ? "
                        "GROUP BY telegram_id ORDER BY time_result) "
                        "AS leaderboard JOIN users "
                        "WHERE "
                        "users.telegram_id = leaderboard.telegram_id",
                        (movement,)
                    ).fetchall()
                else:
                    movement_leaderboard = self.cursor.execute(
                        "SELECT "
                        "users.username, users.first_name, users.last_name, "
                        "users.level, leaderboard.result, "
                        "leaderboard.latest_date "
                        "FROM "
                        "(SELECT "
                        "telegram_id, movement,"
                        " result, "
                        "MAX(DATE(date)) AS latest_date "
                        "FROM aerobic_capacity WHERE movement = ? "
                        "GROUP BY telegram_id ORDER BY result DESC) "
                        "AS leaderboard JOIN users "
                        "WHERE "
                        "users.telegram_id = leaderboard.telegram_id",
                        (movement,)
                    ).fetchall()
                return movement_leaderboard
        except ValueError:
            return 'Нету данных!'

    async def metcon_leaderboard(self, metcon: str) -> [tuple, str]:
        """

        :param metcon:
        :return:
        """
        time_metcons = ['150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                        'Калсу', 'Open 16.5']
        try:
            with self.connection:
                if metcon in time_metcons:
                    metcon_leaderboard = self.cursor.execute(
                        "SELECT "
                        "users.username, users.first_name, users.last_name, "
                        "users.level, leaderboard.result_time, "
                        "leaderboard.latest_date "
                        "FROM "
                        "(SELECT "
                        "telegram_id, metcon,"
                        " result_time, "
                        "MAX(DATE(date)) AS latest_date "
                        "FROM metcons WHERE metcon = ? "
                        "GROUP BY telegram_id ORDER BY result_time) "
                        "AS leaderboard JOIN users "
                        "WHERE "
                        "users.telegram_id = leaderboard.telegram_id",
                        (metcon,)
                    ).fetchall()
                else:
                    metcon_leaderboard = self.cursor.execute(
                        "SELECT "
                        "users.username, users.first_name, users.last_name, "
                        "users.level, leaderboard.result_reps, "
                        "leaderboard.latest_date "
                        "FROM "
                        "(SELECT "
                        "telegram_id, metcon,"
                        " result_reps, "
                        "MAX(DATE(date)) AS latest_date "
                        "FROM metcons WHERE metcon = ? "
                        "GROUP BY telegram_id ORDER BY result_reps DESC) "
                        "AS leaderboard JOIN users "
                        "WHERE "
                        "users.telegram_id = leaderboard.telegram_id",
                        (metcon,)
                    ).fetchall()
                return metcon_leaderboard
        except ValueError:
            return 'Нету данных!'

    async def gymnastics_movements_leaderboard(
            self, movement: str) -> [tuple, str]:
        """
        Get leaderboard for chosen gymnastics movement by user.
        :param movement:
        :return:
        """
        try:
            with self.connection:
                movement_leaderboard = self.cursor.execute(
                    f"SELECT users.username, users.first_name, users.last_name,"
                    f" users.level, leaderboard.result, leaderboard.latest_date"
                    f" FROM "
                    f"(SELECT telegram_id, movement, result, MAX(DATE(date)) "
                    f"AS latest_date FROM gymnastics WHERE movement =? "
                    f"GROUP BY telegram_id ORDER BY result DESC) "
                    f"AS leaderboard JOIN users "
                    f"WHERE "
                    f"users.telegram_id = leaderboard.telegram_id", (movement,)
                ).fetchall()
            return movement_leaderboard
        except ValueError:
            return 'Нету данных!'

    async def update_user_weight(self, telegram_id: int, state: FSMContext):
        """
        Update user weight by telegram_id in user_table
        :param telegram_id: int
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users SET weight = ?"
                    "WHERE telegram_id = ?", (data['weight'], telegram_id)
                )

    async def update_user_height(self, telegram_id: int, state: FSMContext):
        """
        Update user height by telegram_id in user_table.
        :param telegram_id: int
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users SET height = ?"
                    "WHERE telegram_id = ?", (data['height'], telegram_id)
                )

    async def update_user_birthdate(self, telegram_id: int, state: FSMContext):
        """
        Update_user_birthdate
        :param telegram_id:
        :param state:
        :return:
        """
        async with state.proxy() as data:
            self.cursor.execute(
                " UPDATE users SET birthdate = ?"
                " WHERE telegram_id = ?", (data['birthdate'], telegram_id)
            )

    async def update_strength_movement(self, state: FSMContext):
        """
        Update user movement result in strength table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO strength(telegram_id, movement, result, date)"
                    "VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_power_movement(self, state: FSMContext) -> None:
        """
        Update power movement im explosive_power_table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    "explosive_power(telegram_id, movement, result, date)"
                    "VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_strength_capacity_movement(
            self, state: FSMContext) -> None:
        """
        Update strength capacity movement in strength_cap_table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    "strength_capacity(telegram_id, movement,"
                    " result_reps, result_weight, koef_Sinkler, date)"
                    " VALUES (?, ?, ?, ?, ?, ?)", tuple(data.values())
                )

    async def update_time_result_aerobic_movement(
            self, state: FSMContext) -> None:
        """
        Adds data row with time result to aerobic table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    "aerobic_capacity(telegram_id, movement, time_result, date)"
                    " VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_time_result_metcon(self, state: FSMContext) -> None:
        """
        Adds data row with time result to metcon table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    " metcons(telegram_id, metcon, result_time, date)"
                    " VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_result_aerobic_movement(self, state: FSMContext) -> None:
        """
        Adds data row with result to aerobic table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    "aerobic_capacity(telegram_id, movement, result, date)"
                    " VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_metcon_result(self, state: FSMContext) -> None:
        """
        Adds data row with reps result to metcon table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    " INSERT INTO "
                    " metcons(telegram_id, metcon, result_reps, date)"
                    " VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def update_gymnastics_movement(self, state: FSMContext) -> None:
        """
        Adds data row with result to gymnastics table.
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO "
                    "gymnastics(telegram_id, movement, result, date)"
                    " VALUES (?, ?, ?, ?)", tuple(data.values())
                )

    async def add_workout_result(self, state: FSMContext) -> None:
        """
        Adds new workout result in workout_history_table
        :param state:
        :return:
        """
        async with state.proxy() as data:
            with self.connection:
                self.cursor.execute(
                    "INSERT INTO workout_history(telegram_id, results, hashtag)"
                    "VALUES (?, ?, ?)", tuple(data.values())
                )

    async def check_and_return_workout_result(
            self,
            telegram_id: int,
            workout_hashtag: str
    ):
        """

        :param telegram_id:
        :param workout_hashtag:
        :return:
        """
        return_data = (False, None)
        with self.connection:
            workout_result = self.cursor.execute(
                "SELECT results "
                "FROM workout_history "
                "WHERE telegram_id = ? AND hashtag = ?", (telegram_id,
                                                          workout_hashtag)
            ).fetchone()
            if workout_result is not None:
                return_data = True, workout_result[0]
        return return_data

    async def get_workout_result_by_hashtag(
            self, workout_hastag: str) -> [tuple, str]:
        try:
            with self.connection:
                workout_results = self.cursor.execute(
                    "SELECT users.username, users.first_name,"
                    " users.last_name, workouts.results "
                    "FROM (SELECT * FROM workout_history WHERE hashtag = ?) "
                    "AS workouts JOIN users "
                    "WHERE users.telegram_id = workouts.telegram_id",
                    (workout_hastag,)
                ).fetchall()
            return workout_results
        except ValueError:
            return "Нету данных!"

    # ОПЕРАЦИЯ НАД ПОЛЬЗОВАТЕЛЯМИ ДЛЯ АДМИНКИ
    async def get_user_info(self, name: str):
        """
        Get users info by name or surname for admin.
        :param name:
        :return:
        """
        with self.connection:
            users_info = self.cursor.execute(
                " SELECT telegram_id, first_name, last_name, level,"
                " subscribtion_date, username, registration_date, birthdate"
                " FROM users"
                " WHERE first_name LIKE ?"
                " OR last_name LIKE ?", (name + '%', name + '%')
            ).fetchall()
        return users_info

    async def get_inactive_users_info(self):
        """
        Get list of inactive user info.
        """
        today = datetime.now().date()
        with self.connection:
            users_info = self.cursor.execute(
                " SELECT telegram_id, first_name, last_name, level,"
                " subscribtion_date, username, registration_date, birthdate"
                " FROM users "
                " WHERE sub_status IS FALSE"
            ).fetchall()
        return users_info

    async def get_user_username(self, telegram_id: int):
        """
        Checks user username
        :param telegram_id:
        :return:
        """
        with self.connection:
            user_username = self.cursor.execute(
                "SELECT username "
                "FROM users "
                "WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
        print(len(user_username[0]))
        return len(user_username[0])

    async def insert_user_username(self,
                                   telegram_id: int,
                                   username: str):
        """
        Inserts username for user.
        :param telegram_id:
        :param username:
        :return:
        """
        try:
            with self.connection:
                self.cursor.execute(
                    "UPDATE users "
                    "SET username = ? "
                    "WHERE telegram_id = ?", (username, telegram_id)
                )
        except ValueError:
            logging.info('Нет такого пользователя', telegram_id)

    async def update_chosen_users(self,
                                  state: FSMContext,
                                  telegram_id: int) -> None:
        """
        Update search phrase for users by admin.
        :param state:
        :param telegram_id:
        :return:
        """
        try:
            async with state.proxy() as data:
                with self.connection:
                    self.cursor.execute(
                        "UPDATE users "
                        "SET chosen_users = ?"
                        "WHERE telegram_id = ?",
                        (data['chosen_users'], telegram_id)
                    )
        except TypeError or ValueError:
            logging.info('Или не string или такого админа нет!', telegram_id)

    async def get_chosen_users(self,
                               telegram_id: int) -> list:
        """
        Returns data from chosen_user column for admin by his telegram_id.
        :param state:
        :param telegram_id:
        :return:
        """
        try:
            with self.connection:
                search_phrase = self.cursor.execute(
                    "SELECT chosen_users "
                    "FROM users WHERE telegram_id = ?", (telegram_id,)
                ).fetchone()
            result = await self.get_user_info(search_phrase[0])
            return result
        except TypeError or ValueError:
            logging.info('Нет данных или не тот тип', telegram_id)

    async def get_today_birthday_users(self) -> list:
        """
        Return first name last name and nickname of users if it's their
        birthday today.
        """
        try:
            with self.connection:
                with self.connection:
                    tomorrow_date = (
                            datetime.now() + timedelta(
                        days=1)).strftime('%m-%d')
                    birthday_users = self.cursor.execute(
                        "SELECT username, first_name, last_name "
                        "FROM users "
                        f"WHERE strftime('%m-%d', birthdate) = ?",
                        (tomorrow_date,)
                    ).fetchall()
            return birthday_users
        except TypeError or ValueError:
            logging.info('Шляпа с ДР!')

    async def get_workout_for_test_day(self, test_workout_id: int) -> str:
        """
        Returns test workout for user by his test_workout_id.
        """
        try:
            with self.connection:
                test_workout = self.cursor.execute(
                    "SELECT test_workout "
                    "FROM test_workouts "
                    "WHERE test_day_id = ?", (test_workout_id,)
                ).fetchone()
                return test_workout[0]
        except ValueError:
            logging.info('Нет такого id для тестового дня!')

    async def get_telegram_ids_of_active_users(self):
        try:
            with self.connection:
                telegram_ids = self.cursor.execute(
                    "SELECT telegram_id "
                    "FROM users "
                    "WHERE  sub_status = True"
                ).fetchall()
            return list(user_id[0] for user_id in telegram_ids)
        except ValueError:
            logging.info('Нету активных пользователей!')

    async def get_telegram_ids_who_answered(self):
        try:
            with self.connection:
                answered_ids = self.cursor.execute(
                    "SELECT telegram_id "
                    "FROM in_progress_from "
                ).fetchall()
            return list(user_id[0] for user_id in answered_ids)
        except ValueError:
            logging.info('Нету активных пользователей!')

    async def get_user_gender(self, telegram_id: int) -> str:
        with self.connection:
            user_gender = self.cursor.execute(
                "SELECT gender"
                " FROM users"
                " WHERE telegram_id = ?", (telegram_id,)
            ).fetchone()
        return user_gender[0]

    async def add_new_data_about_time_in_project(
            self,
            telegram_id: int,
            start_date: str) -> None:
        gender = await self.get_user_gender(telegram_id)
        with self.connection:
            self.cursor.execute(
                "INSERT INTO in_progress_from(telegram_id, start_date, gender) "
                "VALUES (?, ?, ?)", (telegram_id, start_date, gender)
            )
        logging.info(
            f'Added new start date {start_date} for user {telegram_id}')

    async def get_data_about_time_in_project(self) -> list:
        with self.connection:
            data = self.cursor.execute(
                "SELECT start_date, gender "
                "FROM in_progress_from"
            ).fetchall()
        logging.info(f'Data: {data}')
        return data

    async def get_birthdate_of_active_users(self) -> [list, list]:
        """
        Returns birthdates of active users divided by gender.
        """
        today = date.today()
        men_age = []
        with self.connection:
            men_data = self.cursor.execute(
                "SELECT birthdate "
                "FROM users "
                "WHERE gender = 'Мужской' AND "
                "sub_status is TRUE"
            ).fetchall()
            women_data = self.cursor.execute(
                "SELECT birthdate "
                "FROM users "
                "WHERE gender = 'Женский' AND "
                "sub_status is TRUE"
            ).fetchall()
        return men_data, women_data

    async def add_data_to_weekly_table(self,):
