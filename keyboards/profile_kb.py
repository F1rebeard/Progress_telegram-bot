from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.user_kb import create_inline_keyboard
from handlers.aerobic_capacity import seconds_to_time_string
from create_bot import db


PROFILE_CATEGORIES_BTN = (
    ('Биометрика', 'biometrics'),
    ('Сила', 'strength'),
    ('Взрывная сила', 'power'),
    ('Силовая выносливость', 'strength_capacity'),
    ('Выносливость, эргометры', 'aerobic_capacity'),
    ('Гимнастика', 'gymnastics'),
    ('Метконы', 'metcons')
)

STRENGTH_INLINE_BTNS = {
    'Фронтальный присед 1ПМ':
        ['front_squat', 'front_squat_hst', 'front_squat_score', 'кг'],
    'Присед 1ПМ':
        ['back_squat', 'back_squat_hst', 'back_squat_score', 'кг'],
    'Оверхед присед 1ПМ':
        ['overhead_squat', 'overhead_squat_hst', 'overhead_squat_score', 'кг'],
    'Жим стоя 1ПМ':
        ['push_press', 'push_press_hst', 'push_press_score', 'кг'],
    'Жим лежа 1ПМ':
        ['bench_press', 'bench_press_hst', 'bench_press_score', 'кг'],
    'Cтановая тяга 1ПМ':
        ['deadlift', 'deadlift_hst', 'deadlift_score', 'кг'],
    'Тяга в толчковых углах 1ПМ':
        ['clean_lift', 'clean_lift_hst', 'clean_lift_score', 'кг'],
    'Тяга в рывковых углах 1ПМ':
        ['snatch_lift', 'snatch_lift_hst', 'snatch_lift_score', 'кг']

}

EXPLOSIVE_POWER_INLINE_BTNS = {
    'Прыжок в длину':
        ['long_jump', 'long_jump_hst', 'long_jump_score', 'см'],
    'Рывок с пола в сед':
        ['snatch', 'snatch_hst', 'snatch_score', 'кг'],
    'Рывок с пола в стойку':
        ['power_snatch', 'power_snatch_hst', 'power_snatch_score', 'кг'],
    'Рывок с виса в сед':
        ['hang_snatch', 'hang_snatch_hst', 'hang_snatch_score', 'кг'],
    'Рывок с виса в стойку':
        ['hang_power_snatch', 'hang_power_snatch_hst',
         'hang_power_snatch_score', 'кг'],
    'Подъем на грудь с пола в сед':
        ['clean', 'clean_hst', 'clean_score', 'кг'],
    'Подъем на грудь с пола в стойку':
        ['power_clean', 'power_clean_hst', 'power_clean_score', 'кг'],
    'Жимовой швунг':
        ['power_jerk', 'power_jerk_hst', 'power_jerk_score', 'кг'],
    'Толчковый швунг':
        ['jerk', 'jerk_hst', 'jerk_score', 'кг'],
    'Толчок в ножницы':
        ['split_jerk', 'split_jerk_hst', 'split_jerk_score', 'кг'],
    'Трастер со стоек':
        ['thruster', 'thruster_hst', 'thruster_score', 'кг'],
    'Кластер с пола':
        ['cluster', 'cluster_hst', 'cluster_score', 'кг']
}

STRENGTH_CAPACITY_INLINE_BTNS = {
    'Становая 70% от 1ПМ на кол-во':
        ['deadlift_cpt', 'deadlift_cpt_hst', 'deadlift_cpt_score', 'пвт'],
    'Присед 70% от 1ПМ на кол-во':
        ['squat_cpt', 'squat_cpt_hst', 'squat_cpt_score', 'пвт'],
    'Жим стоя 70% от 1ПМ на кол-во':
        ['push_press_cpt', 'push_press_cpt_hst',
         'push_press_cpt_score', 'пвт'],
    'Жим лежа 70% от 1ПМ на кол-во':
        ['bench_press_cpt', 'bench_press_cpt_hst',
         'bench_press_cpt_score', 'пвт'],
    'Подтягивания с подвесом на кол-во':
        ['pull_up_cpt', 'pull_up_cpt_hst', 'pull_up_cpt_score', 'пвт'],
    'Отжимания  с подвесом на кол-во':
        ['deeps_cpt', 'deeps_cpt_hst', 'deeps_cpt_score', 'пвт']
}

AEROBIC_CAPACITY_INLINE_BTNS = {
    'Гребля 2 км':
        ['2_km_row', '2_km_row_hst', '2_km_row_score', '⏱️'],
    'Гребля 5 км':
        ['5_km_row', '5_km_row_hst', '5_km_row_score', '⏱️'],
    'Гребля 10 км':
        ['10_km_row', '10_km_row_hst', '10_km_row_score', '⏱️'],
    'Гребля ступенчатый':
        ['row_step', 'row_step_hst', 'row_step_score', 'ватт'],
    'Гребля МАМ':
        ['row_mam', 'row_mam_hst', 'row_mam_score', 'ватт'],
    'Гребля 1 час':
        ['row_1_hour', 'row_1_hour_hst', 'row_1_hour_score', 'м'],
    'Гребля 10 минут':
        ['row_10_min', 'row_10_min_hst', 'row_10_min_score', 'кал'],
    'Байк ступенчатый':
        ['bike_step', 'bike_step_hst', 'bike_step_score', 'ватт'],
    'Байк МАМ':
        ['bike_mam', 'bike_mam_hst', 'bike_mam_score', 'ватт'],
    'Байк 10 минут':
        ['bike_10_min', 'bike_10_min_hst', 'bike_10_min_score', 'кал'],
    'Лыжи ступенчатый':
        ['skierg_step', 'skierg_step_hst', 'skierg_step_score', 'ватт'],
    'Лыжи МАМ':
        ['skierg_mam', 'skierg_mam_hst', 'skierg_mam_score', 'ватт'],
    'Лыжи 10 минут':
        ['skierg_10_min', 'skierg_10_min_hst', 'skierg_10_min_score', 'кал']
}

GYMNASTICS_INLINE_BTNS = {
    'Строгие подтягивания 1ПМ':
        ['pull_up_1_rm', 'pull_up_1rm_hst', 'pull_up_1rm_score', 'кг'],
    'Отжимания на кольцах 1ПМ':
        ['ring_deep_1_rm', 'ring_deep_1_rm_hst', 'ring_deep_1_rm_score', 'кг'],
    'Отжимания на брусьях 1ПМ':
        ['deep_1rm', 'deep_1rm_hst', 'deep_1_rm_score', 'кг'],
    'Подтягивания за 1 подход':
        ['pull_ups', 'pull_ups_hst', 'pull_ups_score', 'пвт'],
    'Строгие отжимания в стойке за 1 подход':
        ['strict_hs_push_ups', 'strict_hs_push_ups_hst',
         'strict_hs_push_ups_score', 'пвт'],
    'Отжимания в стойке кипом за 1 подход':
        ['hs_push_ups', 'hs_push_ups_hst', 'hs_push_ups_score', 'пвт'],
    'Строгие выходы на кольцах за 1 подход':
        ['strict_ring_muscle_ups', 'strict_ring_muscle_ups_hst',
         'strict_ring_muscle_ups_score', 'пвт'],
    'Выходы на кольцах за 1 подход':
        ['ring_muscle_ups', 'ring_muscle_ups_hst',
         'ring_muscle_ups_score', 'пвт'],
    'Выходы на кольцах за 90 секунд':
        ['90_sec_ring_muscle_ups', '90_sec_ring_muscle_ups_hst',
         '90_sec_ring_muscle_ups_score', 'пвт'],
    'Выходы на перекладине за 1 подход':
        ['muscle_ups', 'muscle_ups_hst', 'muscle_ups_score', 'пвт'],
    'Выходы на перекладине за 90 секунд':
        ['90_sec_muscle_ups', '90_sec_muscle_ups_hst',
         '90_sec_muscle_ups_score', 'пвт'],
    'НКП за 1 подход':
        ['t2b', 't2b_hst', 't2b_score', 'пвт'],
    'Канаты 4.5 метра с ногами за 2 минуты':
        ['ropes', 'ropes_hst', 'ropes_score', 'пвт'],
    'Канаты 4.5 метра без ног за 2 минуты':
        ['legless_ropes', 'legless_ropes_hst', 'legless_ropes_score', 'пвт'],
    'Уголок в упоре на полу':
        ['l_sit', 'l_sit_hst', 'l_sit_score', 'c'],
    'Вис в уголке':
        ['hang_l_sit', 'hang_l_sit_hst', 'hang_l_sit_score', 'c'],
    'Вис на перекладине':
        ['hang', 'hang_hst', 'hang_score', 'c'],
    'Ходьба на руках за 1 проход':
        ['hs_walk', 'hs_walk_hst', 'hs_walk_score', 'м'],
    'Ходьба на руках за 1 минуту':
        ['min_hs_walk', 'min_hs_walk_hst', 'min_hs_walk_score', 'м']
}

METCONS_INLINE_KB = {
    '150 бурпи с прыжком +15 см':
        ['150_burpees', '150_burpees_hst', '150_burpees_score', '⏱️',
         '150_burpees_desc'],
    'Карен':
        ['karen', 'karen_hst', 'karen_score', '⏱️',
         'karen_desc'],
    'Мерф':
        ['murph', 'murph_hst', 'murph_score', '⏱️',
         'murph_desc'],
    'Синди':
        ['cindy', 'cindy_hst', 'cindy_score', 'пвт', 'cindy_desc'],
    'Линда':
        ['linda', 'linda_hst', 'linda_score', '⏱️', 'linda_desc'],
    'Open 13.1':
        ['open_13_1', 'open_13_1_hst', 'open_13_1_score', 'пвт',
         'open_13_1_desc'],
    'Калсу':
        ['kalsu', 'kalsu_hst', 'kalsu_score', '⏱️', 'kalsu_desc'],
    'Open 19.1':
        ['open_19_1', 'open_19_1_hst', 'open_19_1_score', 'пвт',
         'open_19_1_desc'],
    'Open 16.5':
        ['open_16_5', 'open_16_5_hst', 'open_16_5_score', '⏱️',
         'open_16_5_desc']
}

categories_keyboard = create_inline_keyboard(PROFILE_CATEGORIES_BTN)


async def fill_keyboard_with_data(
        data: tuple,
        buttons: dict,
        inline_keyboard: InlineKeyboardMarkup
) -> InlineKeyboardMarkup:
    """
    Fills inline keyboard with data from database.
    :param data:
    :param buttons:
    :param inline_keyboard:
    :return:
    """
    for index in range(len(data)):
        inline_keyboard.row()
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'{data[index][0]}',
                callback_data=buttons.get(data[index][0])[0]
            )
        )
        inline_keyboard.row()
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'{data[index][2]} '
                f'{buttons.get(data[index][0])[3]}',
                callback_data=buttons.get(data[index][0])[0]
            )
        )
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'История',
                callback_data=buttons.get(data[index][0])[1]
            )
        )
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'Лидерборд',
                callback_data=buttons.get(data[index][0])[2]
            )
        )
    return inline_keyboard


async def fill_empty_keyboard(
        data: tuple,
        buttons: dict,
        inline_keyboard: InlineKeyboardMarkup
) -> InlineKeyboardMarkup:
    """
    Fills inline keyboard without data from database.
    :param data:
    :param buttons:
    :param inline_keyboard:
    :return:
    """
    # creates list on movement names without data from database
    no_result_movements = []
    # getting movement names
    temp = list(buttons.keys())
    for key in temp:
        if key not in [row[0] for row in data]:
            no_result_movements.append(key)
    for index in range(len(no_result_movements)):
        buttons_data = buttons.get(no_result_movements[index])
        print(buttons_data)
        inline_keyboard.row()
        if buttons == METCONS_INLINE_KB:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    f'{no_result_movements[index]}',
                    callback_data=buttons_data[4]
                )
            )
        else:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    f'{no_result_movements[index]}',
                    callback_data=buttons_data[0]
                )
            )
        inline_keyboard.row()
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'Нет данных',
                callback_data=buttons_data[0]
            )
        )
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'История',
                callback_data=buttons_data[1]
            )
        )
        inline_keyboard.insert(
            InlineKeyboardButton(
                f'Лидерборд',
                callback_data=buttons_data[2]
            )
        )
    return inline_keyboard


async def history_data(data: tuple, movement: str, keyboard: dict) -> str:
    """
    Transforms data from database for correct
     movement history presentation in message.
    :param data:
    :param movement:
    :param keyboard:
    :return:
    """
    time_movements = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км',
                      '150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                      'Калсу', 'Open 16.5']
    if keyboard == STRENGTH_CAPACITY_INLINE_BTNS:
        result: str = f'{movement}:\n\n{"Дата": <15} ' \
                      f'{"Результат, кг * пвт": >15}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                result = result + f'{rows[0]: <15} ' \
                                  f'{rows[2]: >15} * {rows[1]}\n'
    elif movement in time_movements:
        result: str = f'{movement}:\n\n{"Дата": <15} ' \
                      f'{"Результат, " + list(keyboard.get(movement))[3]: >15}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                converted_data = seconds_to_time_string(rows[1])
                result = result + f'{rows[0]: <15} {converted_data: >15}\n'
    else:
        result: str = f'{movement}:\n\n{"Дата": <15} ' \
                      f'{"Результат, " + list(keyboard.get(movement))[3]: >15}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                result = result + f'{rows[0]: <15} {rows[1]: >15}\n'
    return result


async def leaderboard_data(data: tuple, movement: str, keyboard: dict) -> str:
    """
    Transforms data from database
    :param data:
    :param movement:
    :param keyboard:
    :return:
    """
    time_movements = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км',
                      '150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                      'Калсу', 'Open 16.5']
    if keyboard == STRENGTH_CAPACITY_INLINE_BTNS:
        result: str = f'{movement}: \n\n'\
                  f'{"📈 коэф.": <10} ' \
                  f'{"🏋️": <40} {"Ур.": >0}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                # rows[4] - result, rows[3] - user level
                # rows[0] - telegram nickname
                # rows[1] - first name, rows[2] - last name
                name_letter: str = rows[1][0:1].title()
                athlete = f'{rows[2]} {name_letter}. @{rows[0]}'
                result = result + f'{rows[4]: <8} {athlete: <25} {rows[3]: >0}\n'
    elif movement in time_movements:
        result: str = f'{movement}: \n\n' \
                      f'{"📈, " + list(keyboard.get(movement))[3]: <10} ' \
                      f'{"🏋️": <40} {"Ур.": >0}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                # rows[4] - result, rows[3] - user level
                # rows[0] - telegram nickname
                # rows[1] - first name, rows[2] - last name
                data = seconds_to_time_string(rows[4])
                name_letter: str = rows[1][0:1].title()
                athlete = f'{rows[2]} {name_letter}. @{rows[0]}'
                result = result + f'{data: <8} {athlete: <25} {rows[3]: >0}\n'
    else:
        result: str = f'{movement}: \n\n'\
                      f'{"📈, " + list(keyboard.get(movement))[3]: <10} ' \
                      f'{"🏋️": <40} {"Ур.": >0}\n'
        if len(data) == 0:
            result = result + 'Пока нету данных!'
        else:
            for rows in data:
                # rows[4] - result, rows[3] - user level
                # rows[0] - telegram nickname
                # rows[1] - first name, rows[2] - last name
                name_letter: str = rows[1][0:1].title()
                athlete = f'{rows[2]} {name_letter}. @{rows[0]}'
                result = result + f'{rows[4]: <8} {athlete: <25} {rows[3]: >0}\n'
    return result


async def biometrics_inline_btns(telegram_id: int) -> tuple:
    """
    Creates biometrics parameters inline keyboard.
    :param telegram_id:
    :return:
    """
    user_biometrics = await db.get_user_biometrics(telegram_id)
    biometrics_inline_btns = (
            (f'Уровень: {user_biometrics[0]}', 'level'),
            (f'Рост: {user_biometrics[2]} cм', 'height'),
            (f'Вес: {user_biometrics[3]} кг', 'weight'),
            (f'Дата рождения: {user_biometrics[4]}', 'birthdate')
        )
    return biometrics_inline_btns


async def strength_inline_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру из силовых движений с результатами пользователя
    по id в телеграмме. В случае отсутствия данных выводит кнопки только
    с названием сообщений, если же данные добавлены в базу данных,
    то выводит ряд из кнопок с названием и
    последним результатом упражнения.
    :param telegram_id:
    :return:
    """
    # делаем запрос в бд
    strength_data = await db.get_user_last_strength_result(telegram_id)
    inline_kb = InlineKeyboardMarkup(row_width=3)
    # создаём кнопки с данными из бд
    await fill_keyboard_with_data(
        data=strength_data,
        buttons=STRENGTH_INLINE_BTNS,
        inline_keyboard=inline_kb
    )
    # проверка количества движений из бд пользователя к общему количеству
    if len(strength_data) < len(STRENGTH_INLINE_BTNS):
        await fill_empty_keyboard(
            data=strength_data,
            buttons=STRENGTH_INLINE_BTNS,
            inline_keyboard=inline_kb,
        )
    return inline_kb


async def power_inline_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн клавиатуру для ТА движений с результатами пользователя
    по id в телеграмме. В случае отсутствия данных выводит кнопки только
    с названием сообщений, если же данные добавлены в базу данных,
    то выводит ряд из кнопок с названием и
    последним результатом упражнения.
    :param telegram_id:
    :return:
    """
    explosive_power_data = await db.get_user_last_power_result(telegram_id)
    inline_kb = InlineKeyboardMarkup(row_width=3)
    await fill_keyboard_with_data(
        data=explosive_power_data,
        buttons=EXPLOSIVE_POWER_INLINE_BTNS,
        inline_keyboard=inline_kb
    )
    if len(explosive_power_data) < len(EXPLOSIVE_POWER_INLINE_BTNS):
        await fill_empty_keyboard(
            data=explosive_power_data,
            buttons=EXPLOSIVE_POWER_INLINE_BTNS,
            inline_keyboard=inline_kb,
        )
    return inline_kb


async def strength_capacity_inline_keyboard(
        telegram_id: int) -> InlineKeyboardMarkup:
    """

    :param telegram_id:
    :return:
    """
    strength_cpt_data = await db.get_user_last_strength_capacity_result(
        telegram_id
    )
    inline_kb = InlineKeyboardMarkup(row_width=3)
    for i in range(len(strength_cpt_data)):
        inline_kb.row()
        inline_kb.insert(
            InlineKeyboardButton(
                f'{strength_cpt_data[i][0]}',
                callback_data=STRENGTH_CAPACITY_INLINE_BTNS.get(
                    strength_cpt_data[i][0])[0]
            )
        )
        inline_kb.row()
        inline_kb.insert(
            InlineKeyboardButton(
                text=f'{int(strength_cpt_data[i][3])} кг / '
                     f'{strength_cpt_data[i][2]}'
                     f' {STRENGTH_CAPACITY_INLINE_BTNS.get(strength_cpt_data[i][0])[3]}',
                callback_data=STRENGTH_CAPACITY_INLINE_BTNS.get(
                    strength_cpt_data[i][0])[0]
            )
        )
        inline_kb.insert(
            InlineKeyboardButton(
                f'История',
                callback_data=STRENGTH_CAPACITY_INLINE_BTNS.get(
                    strength_cpt_data[i][0])[1]
            )
        )
        inline_kb.insert(
            InlineKeyboardButton(
                f'Лидерборд',
                callback_data=STRENGTH_CAPACITY_INLINE_BTNS.get(
                    strength_cpt_data[i][0])[2]
            )
        )
    if len(strength_cpt_data) < len(STRENGTH_CAPACITY_INLINE_BTNS):
        await fill_empty_keyboard(
            data=strength_cpt_data,
            buttons=STRENGTH_CAPACITY_INLINE_BTNS,
            inline_keyboard=inline_kb,
        )
    return inline_kb


async def aerobic_inline_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Creates inline keyboard for aerobic capacity movements in aerobic capacity
    category.
    :param telegram_id:
    :return:
    """
    aerobic_data = await db.get_user_last_aerobic_result(telegram_id)
    time_movements = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км']
    inline_kb = InlineKeyboardMarkup(row_width=3)
    for i in range(len(aerobic_data)):
        inline_kb.row()
        inline_kb.insert(
            InlineKeyboardButton(
                f'{aerobic_data[i][0]}',
                callback_data=AEROBIC_CAPACITY_INLINE_BTNS.get(
                    aerobic_data[i][0]
                )[0]
            )
        )
        inline_kb.row()
        if aerobic_data[i][0] in time_movements:
            inline_kb.insert(
                InlineKeyboardButton(
                    f'{seconds_to_time_string(aerobic_data[i][3])} '
                    f'{AEROBIC_CAPACITY_INLINE_BTNS.get(aerobic_data[i][0])[3]}',
                    callback_data=AEROBIC_CAPACITY_INLINE_BTNS.get(
                        aerobic_data[i][0]
                    )[0]
                )
            )
        else:
            inline_kb.insert(
                InlineKeyboardButton(
                    f'{aerobic_data[i][2]} '
                    f'{AEROBIC_CAPACITY_INLINE_BTNS.get(aerobic_data[i][0])[3]}',
                    callback_data=AEROBIC_CAPACITY_INLINE_BTNS.get(
                        aerobic_data[i][0]
                    )[0]
                )
            )
        inline_kb.insert(
            InlineKeyboardButton(
                f'История',
                callback_data=AEROBIC_CAPACITY_INLINE_BTNS.get(
                    aerobic_data[i][0]
                )[1]
            )
        )
        inline_kb.insert(
            InlineKeyboardButton(
                f'Лидерборд',
                callback_data=AEROBIC_CAPACITY_INLINE_BTNS.get(
                    aerobic_data[i][0]
                )[2]
            )
        )
        # проверка количества движений из бд пользователя к общему количеству
    if len(aerobic_data) < len(AEROBIC_CAPACITY_INLINE_BTNS):
        await fill_empty_keyboard(
            data=aerobic_data,
            buttons=AEROBIC_CAPACITY_INLINE_BTNS,
            inline_keyboard=inline_kb,
        )
    return inline_kb


async def gymnastics_inline_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн клавиатуру для гимнастики с результатами пользователя
    по id в телеграмме. В случае отсутствия данных выводит кнопки только
    с названием сообщений, если же данные добавлены в базу данных,
    то выводит ряд из кнопок с названием и
    последним результатом упражнения.
    :param telegram_id:
    :return:
    """
    gymnastics_data = await db.get_user_last_gymnastics_result(telegram_id)
    inline_kb = InlineKeyboardMarkup(row_width=3)
    await fill_keyboard_with_data(
        data=gymnastics_data,
        buttons=GYMNASTICS_INLINE_BTNS,
        inline_keyboard=inline_kb
    )
    if len(gymnastics_data) < len(GYMNASTICS_INLINE_BTNS):
        await fill_empty_keyboard(
            data=gymnastics_data,
            buttons=GYMNASTICS_INLINE_BTNS,
            inline_keyboard=inline_kb
        )
    return inline_kb


async def metcon_inline_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """
    Creates inline keyboard for metcons.
    :param telegram_id:
    :return:
    """
    metcons_data = await db.get_user_metcons_last_result(telegram_id)
    time_metcons = ['150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                    'Калсу', 'Open 16.5']
    inline_kb = InlineKeyboardMarkup(row_width=3)
    for i in range(len(metcons_data)):
        inline_kb.row()
        inline_kb.insert(
            InlineKeyboardButton(
                f'{metcons_data[i][0]}',
                callback_data=METCONS_INLINE_KB.get(metcons_data[i][0])[4]
            )
        )
        inline_kb.row()
        if metcons_data[i][0] in time_metcons:
            buttons_value = METCONS_INLINE_KB.get(metcons_data[i][0])
            inline_kb.insert(
                InlineKeyboardButton(
                    f'{seconds_to_time_string(metcons_data[i][3])} '
                    f'{buttons_value[3]}',
                    callback_data=buttons_value[0]
                )
            )
        else:
            buttons_value = METCONS_INLINE_KB.get(metcons_data[i][0])
            inline_kb.insert(
                InlineKeyboardButton(
                    f'{metcons_data[i][2]} '
                    f'{buttons_value[3]}',
                    callback_data=buttons_value[0]
                )
            )
        inline_kb.insert(
            InlineKeyboardButton(
                f'История',
                callback_data=buttons_value[1]
            )
        )
        inline_kb.insert(
            InlineKeyboardButton(
                f'Лидерборд',
                callback_data=buttons_value[2]
            )
        )
    if len(metcons_data) < len(METCONS_INLINE_KB):
        await fill_empty_keyboard(
            data=metcons_data,
            buttons=METCONS_INLINE_KB,
            inline_keyboard=inline_kb
        )
    return inline_kb
