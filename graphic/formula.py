import logging

from create_bot import db
from graphic.сonstants import (NINETY_PERCENTS,
                               TEN_PERCENTS,
                               ONE_HUNDRED_PERCENTS,
                               TIME_MOVEMENTS,
                               MINKAIF_LVL_ONE_USERS,
                               MINKAIF_LVL_TWO_USERS,
                               STRENGTH_RANGES,
                               STRENGTH_CAPACITY_RANGES,
                               AEROBIC_RANGES,
                               POWER_RANGES,
                               GYMNASTIC_RANGES,
                               METCON_RANGES,
                               BASE_METCON_RANGES,
                               BASE_POWER_RANGES,
                               BASE_AEROBIC_RANGES,
                               BASE_STRENGTH_RANGES,
                               BASE_GYMNASTIC_RANGES,
                               BASE_STRENGTH_CAPACITY_RANGES)


async def user_info(telegram_id: int) -> (int, int):
    """
    Get user level and gender from database by telegram id.
    :param telegram_id:
    :return:
    """
    user_data = await db.get_user_biometrics(telegram_id)
    user_level = user_data[0]
    user_gender = user_data[1]
    return user_level, user_gender


async def choose_the_interval(
        telegram_id: int,
        minkaif_lvl_one: list[int],
        minkaif_lvl_two: list[int],
        gender: str,
        user_level: str,
        movement_data: list) -> (int, int):
    """
    Depending on user level and gender chooses correct interval for movements.
    For minkaif users depends on sorted data.
    :param telegram_id: message.from_user.id
    :param minkaif_lvl_one: constant from constants.py
    :param minkaif_lvl_two: constant from constants.py
    :param gender: from database via telegram_id
    :param user_level: from database via telegram_id
    :param movement_data: from database via telegram_id
    :return:
    """
    if user_level == 'Первый' or (telegram_id in minkaif_lvl_one):
        if gender == 'Мужской':
            # 100% value for men (10 from 10)
            one_hundred_perc = movement_data[2]
            # 10% value for men (1 from 10)
            ten_perc = movement_data[1]
            return ten_perc, one_hundred_perc
        if gender == "Женский":
            # 100% value for women (10 from 10)
            one_hundred_perc = movement_data[4]
            # 100% value for women (1 from 10)
            ten_perc = movement_data[3]
            return ten_perc, one_hundred_perc
    elif (user_level == 'Второй' or
            user_level == 'Соревнования' or
            telegram_id in minkaif_lvl_two):
        if gender == 'Мужской':
            # значеник 100% для парней (10 из 10)
            one_hundred_perc = movement_data[6]
            # значение 10% для парней (1 из 10)
            ten_perc = movement_data[5]
            return ten_perc, one_hundred_perc
        if gender == "Женский":
            # значеник 100% для девушек (10 из 10)
            one_hundred_perc = movement_data[8]
            # значение 10% для девушек (1 из 10)
            ten_perc = movement_data[7]
            return ten_perc, one_hundred_perc
    else:
        return None


def time_string_to_seconds(text: str) -> int or str:
    """
    Transforms string message from user like 12:22 where 12 - min and 22 - sec
    to total seconds  for calculation.
    :param text:
    :return:
    """
    try:
        time_split = [int(index) for index in text.split(':')]
        time_split.reverse()
        seconds = sum(
            time_split[index] * 60**index for index in range(len(time_split))
        )
        return seconds
    except ValueError as error:
        raise ValueError('Invalid time string format or content') from error


async def transform_to_float(one_hundred_perc: str,
                             ten_perc: str,
                             user_result: str) -> (float, float, float):
    """
    Transform string or not float data to float for further calculations.
    :param one_hundred_perc:
    :param ten_perc:
    :param user_result:
    :return:
    """
    try:
        hdr_perc_transformed = round(float(one_hundred_perc), 1)
        ten_perc_transformed = round(float(ten_perc), 1)
        result_transformed = round(float(user_result), 1)
        return hdr_perc_transformed, ten_perc_transformed, result_transformed
    except TypeError or ValueError:
        logging.info('Не удалось преобразовать данные!', user_result)


async def movement_result_to_axis_value(one_hundred_perc: float,
                                        ten_perc: float,
                                        user_result: float) -> float:
    """
    Returns value of exercise in percents.
    :param one_hundred_perc:
    :param ten_perc:
    :param user_result:
    :return:
    """
    if user_result < ten_perc:
        one_perc_value = ten_perc / TEN_PERCENTS
        movement_axis_result = user_result / one_perc_value
        if movement_axis_result <= 0:
            return 0
        return movement_axis_result
    elif ten_perc < user_result < one_hundred_perc:
        one_perc_value = (one_hundred_perc - ten_perc) / NINETY_PERCENTS
        movement_axis_result = (
                (user_result - ten_perc) / one_perc_value + TEN_PERCENTS
        )
        return round(float(movement_axis_result), 1)
    elif user_result > one_hundred_perc:
        one_perc_value = (one_hundred_perc - ten_perc) / NINETY_PERCENTS
        movement_axis_result = (
                (user_result - one_hundred_perc) / one_perc_value + 100.0)
        return round(float(movement_axis_result), 1)
    elif user_result == ten_perc:
        return round(float(TEN_PERCENTS), 1)
    elif user_result == one_hundred_perc:
        return 100.0


async def movement_time_result_to_axis_value(one_hundred_perc: float,
                                        ten_perc: float,
                                        user_result: float) -> float:
    """
    Returns value of exercise in percents with time result exercises.
    :param one_hundred_perc:
    :param ten_perc:
    :param user_result:
    :return:
    """
    if user_result > ten_perc:
        one_perc_value = (ten_perc - one_hundred_perc) / NINETY_PERCENTS
        movement_axis_result = (
            TEN_PERCENTS - (user_result - ten_perc) / one_perc_value
        )
        if movement_axis_result <= 0:
            return 0
        return round(float(movement_axis_result), 1)
    elif ten_perc > user_result > one_hundred_perc:
        one_perc_value = (ten_perc - one_hundred_perc) / NINETY_PERCENTS
        movement_axis_result = (
            (ten_perc - user_result) / one_perc_value + TEN_PERCENTS
        )
        return round(float(movement_axis_result), 1)
    elif one_hundred_perc > user_result:
        one_perc_value = (ten_perc - one_hundred_perc) / NINETY_PERCENTS
        movement_axis_result = (
            (user_result - one_hundred_perc) / one_perc_value + ONE_HUNDRED_PERCENTS
        )
        return round(float(movement_axis_result), 1)
    elif user_result == ten_perc:
        return round(float(TEN_PERCENTS), 1)
    elif user_result == one_hundred_perc:
        return 100.0


async def user_axis_value(telegram_id: int,
                          characteristics_ranges: list,
                          user_results: list,
                          category: str) -> (list or float):
    """
    Returns axis value for the user depending on user results.
    :param telegram_id:
    :param user_results:
    :param characteristics_ranges:
    :param category:
    :return:
    """
    # cписок для добавления значений упражнений
    movement_results = []
    # список упражнений, у которых не заполнены результаты
    no_results = []
    user_bio = await user_info(telegram_id)
    if ((telegram_id not in MINKAIF_LVL_ONE_USERS and
            telegram_id not in MINKAIF_LVL_TWO_USERS) and
            user_bio[0] == 'Минкайфа'):
        return None
    else:
        for movement_data in characteristics_ranges:
            for result in user_results:
                if movement_data[0] == result[0]:
                    # получаем диапазоны для упражнений (муж / жен)
                    ten_perc, one_hundred_perc = await choose_the_interval(
                        gender=user_bio[1],
                        user_level=user_bio[0],
                        movement_data=movement_data,
                        minkaif_lvl_one=MINKAIF_LVL_ONE_USERS,
                        minkaif_lvl_two=MINKAIF_LVL_TWO_USERS,
                        telegram_id=telegram_id
                    )
                    if result[0] in TIME_MOVEMENTS:
                        # перевод текс времени в секунды
                        ten_perc = time_string_to_seconds(ten_perc)
                        one_hundred_perc = time_string_to_seconds(
                            one_hundred_perc)
                        # переводим диапазоны и результат в числа для расчёта
                        hdr_perc, ten_perc, user_result = await transform_to_float(
                            one_hundred_perc=one_hundred_perc,
                            ten_perc=ten_perc,
                            user_result=result[3]
                        )
                        movement_perc_score = await movement_time_result_to_axis_value(
                            one_hundred_perc=hdr_perc,
                            ten_perc=ten_perc,
                            user_result=user_result
                        )
                    else:
                        # переводим диапазоны и результат в числа для расчёта
                        hdr_perc, ten_perc, user_result = await transform_to_float(
                            one_hundred_perc=one_hundred_perc,
                            ten_perc=ten_perc,
                            user_result=result[2]
                        )
                        # получаем значение упражнения в процентах
                        movement_perc_score = await movement_result_to_axis_value(
                            one_hundred_perc=hdr_perc,
                            ten_perc=ten_perc,
                            user_result=user_result
                        )
                    movement_results.append(movement_perc_score)
                    break
            else:
                no_results.append(movement_data[0])
    if len(no_results) != 0:
        # указываем категорию с пустыми упражнениями
        category_name = f'{category}:\n'
        movements = ''
        for movement in no_results:
            movements += f'- {movement}\n'
        return category_name + movements
    else:
        axis_score = sum(movement_results) / len(movement_results)
        return round(float(axis_score), 1)


async def get_base_profile_data(user_id: int) -> list:
    """
    Shows basic characteristics graph with base exercsises filled,
    otherwise shows the list of exercsises to fill.
    """
    # list with result for each category
    base_user_profile_data: list = []
    user_categories_data: list = [
        (BASE_STRENGTH_RANGES, await db.get_user_last_strength_result(user_id),
         'Cила'),
        (BASE_POWER_RANGES, await db.get_user_last_power_result(user_id),
         'Взрывная сила'),
        (BASE_STRENGTH_CAPACITY_RANGES,
         await db.get_user_last_strength_capacity_result(user_id),
         'Cиловая выносливость'),
        (BASE_AEROBIC_RANGES, await db.get_user_last_aerobic_result(user_id),
         'Выносливость и эргометры'),
        (BASE_GYMNASTIC_RANGES,
         await db.get_user_last_gymnastics_result(user_id),
         'Гимнастика'),
        (BASE_METCON_RANGES, await db.get_user_metcons_last_result(user_id),
         'Метконы')
    ]
    for category in user_categories_data:
        base_user_profile_data.append(
            await user_axis_value(
                telegram_id=user_id,
                characteristics_ranges=category[0],
                user_results=category[1],
                category=category[2]
            )
        )
    return base_user_profile_data


async def get_full_profile_data(user_id: int) -> list:
    """
    Shows basic characteristics graph with base exercsises filled,
    otherwise shows the list of exercsises to fill.
    """
    full_user_profile_data: list = []
    user_categories_data: list = [
        (STRENGTH_RANGES, await db.get_user_last_strength_result(user_id),
         'Cила'),
        (POWER_RANGES, await db.get_user_last_power_result(user_id),
         'Взрывная сила'),
        (STRENGTH_CAPACITY_RANGES,
         await db.get_user_last_strength_capacity_result(user_id),
         'Cиловая выносливость'),
        (AEROBIC_RANGES, await db.get_user_last_aerobic_result(user_id),
         'Выносливость и эргометры'),
        (GYMNASTIC_RANGES,
         await db.get_user_last_gymnastics_result(user_id),
         'Гимнастика'),
        (METCON_RANGES, await db.get_user_metcons_last_result(user_id),
         'Метконы')
    ]
    for category in user_categories_data:
        full_user_profile_data.append(
            await user_axis_value(
                telegram_id=user_id,
                characteristics_ranges=category[0],
                user_results=category[1],
                category=category[2]
            )
        )
    return full_user_profile_data
