from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import db, bot
from handlers.users import MainMenu
from handlers.strength import StrengthData
from handlers.power import PowerData
from handlers.aerobic_capacity import AerobicData
from handlers.gymnastics import GymnasticsData
from handlers.metcons import MetconsData
from handlers.strength_capacity import StrengthCapacityData, weight_for_movement
from handlers.biometrics import BiometricsData

from keyboards.user_kb import create_inline_keyboard, profile_keyboard_2
from keyboards.profile_kb import (
    biometrics_inline_btns,
    strength_inline_keyboard,
    STRENGTH_INLINE_BTNS,
    power_inline_keyboard,
    strength_capacity_inline_keyboard,
    gymnastics_inline_keyboard,
    EXPLOSIVE_POWER_INLINE_BTNS,
    STRENGTH_CAPACITY_INLINE_BTNS,
    AEROBIC_CAPACITY_INLINE_BTNS,
    GYMNASTICS_INLINE_BTNS,
    aerobic_inline_keyboard,
    METCONS_INLINE_KB,
    metcon_inline_keyboard,
    history_data,
    leaderboard_data)


async def category_records_leaderboards_names() -> list:
    """
    Creates record list, leaderboard list and movements names list for a chosen
    category.
    :return:
    """
    categories_buttons = [
        STRENGTH_INLINE_BTNS,
        EXPLOSIVE_POWER_INLINE_BTNS,
        STRENGTH_CAPACITY_INLINE_BTNS,
        AEROBIC_CAPACITY_INLINE_BTNS,
        GYMNASTICS_INLINE_BTNS,
        METCONS_INLINE_KB
    ]
    result = []
    for buttons in categories_buttons:
        records = [
            data[1] for data in list(buttons.values())
        ]

        leaderboard = [
            data[2] for data in list(buttons.values())
        ]
        movement_names = list(buttons.keys())
        result[:] = [*result, records, leaderboard, movement_names]
    return result


async def choose_category(query: types.CallbackQuery,
                          state: FSMContext):
    """

    :param query:
    :param state:
    :return:
    """
    telegram_id = query.from_user.id
    results_leaderboards_names = await category_records_leaderboards_names()
    # strength category
    strength_records = results_leaderboards_names[0]
    strength_leaderboard = results_leaderboards_names[1]
    strength_movements_names = results_leaderboards_names[2]
    # power category
    power_records = results_leaderboards_names[3]
    power_leaderbord = results_leaderboards_names[4]
    power_movement_names = results_leaderboards_names[5]
    # strength capacity category
    strength_cpt_records = results_leaderboards_names[6]
    strength_cpt_leaderboard = results_leaderboards_names[7]
    strength_cpt_movement_names = results_leaderboards_names[8]
    # aerobic capacity category
    aerobic_capacity_records = results_leaderboards_names[9]
    aerobic_capacity_leaderboard = results_leaderboards_names[10]
    aerobic_movement_names = results_leaderboards_names[11]
    # gymnastics category
    gymnastics_records = results_leaderboards_names[12]
    gymnastics_leaderboard = results_leaderboards_names[13]
    gymnastics_movement_names = results_leaderboards_names[14]
    # metcons category
    metcon_records = results_leaderboards_names[15]
    metcon_leaderbord = results_leaderboards_names[16]
    metcon_names = results_leaderboards_names[17]
    # categories

    if query.data == 'biometrics':
        biometrics_inline_kb = create_inline_keyboard(
            await biometrics_inline_btns(telegram_id))
        await bot.edit_message_text(text=f'{"Биометрия" : ^10}',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=biometrics_inline_kb)
        await query.answer()
    elif query.data == 'strength':
        strength_inline_kb = await strength_inline_keyboard(telegram_id)
        await bot.edit_message_text(text=f'Cила и пауэрлифтинг',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=strength_inline_kb)
        await query.answer()
    elif query.data == 'power':
        power_inline_kb = await power_inline_keyboard(telegram_id)
        await bot.edit_message_text(text='Взрывная сила и тяжелая атлетика',
                                    message_id=query.message.message_id,
                                    chat_id=query.message.chat.id,
                                    reply_markup=power_inline_kb)
        await query.answer()
    elif query.data == 'strength_capacity':
        strength_cpt_kb = await strength_capacity_inline_keyboard(telegram_id)
        await bot.edit_message_text(
            text='Силовая выносливость',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=strength_cpt_kb
        )
        await query.message.answer(
            f'Внимание!\n\n'
            f'Для корректного ввода результатов в этом разделе, сначала'
            f' необходимо добавить свой вес в разделе "Биометрика" и ПМ'
            f' выбранного движения в разделе "Сила" или "Гимнастика".'
        )
        await query.answer()
    elif query.data == 'aerobic_capacity':
        aerobic_kb = await aerobic_inline_keyboard(telegram_id)
        await bot.edit_message_text(
            text='Выносливость и эргометры',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=aerobic_kb
        )
        await query.answer()
    elif query.data == 'gymnastics':
        gymnastics_kb = await gymnastics_inline_keyboard(telegram_id)
        await bot.edit_message_text(
            text='Гимнастика',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=gymnastics_kb
        )
        await query.answer()
    elif query.data == 'metcons':
        metcons_kb = await metcon_inline_keyboard(telegram_id)
        await bot.edit_message_text(
            text='Метконы и Бенчмарки',
            message_id=query.message.message_id,
            chat_id=query.message.chat.id,
            reply_markup=metcons_kb
        )
    # Biometrics category
    # -------------------
    elif query.data == 'level':
        await bot.send_message(telegram_id,
                               'Для смены уровня обратитесь к кураторам',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'height':
        await state.set_state(BiometricsData.height)
        await bot.send_message(telegram_id,
                               'Введи свой рост в сантиметрах:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'weight':
        await state.set_state(BiometricsData.weight)
        await bot.send_message(telegram_id,
                               'Введи свой вес в килограммах:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'birthdate':
        await state.set_state(BiometricsData.birthdate)
        await bot.send_message(telegram_id,
                               'Введи свою дату рождения в формате '
                               'дд-мм-гггг:',
                               reply_markup=profile_keyboard_2)

    # Strength category
    # ----------------
    # result history callback_data
    elif query.data in strength_records:
        # getting movement index for dict with movement names by query.data
        movement_index = strength_records.index(query.data)
        # getting movement name for database from dict
        movement = list(STRENGTH_INLINE_BTNS.keys())[movement_index]
        # getting movement results for user
        movement_history = await db.strength_movement_result_history(
            telegram_id, movement
        )
        # making text for message
        await bot.send_message(telegram_id,
                               text=await history_data(movement_history,
                                                       movement,
                                                       STRENGTH_INLINE_BTNS),
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data in strength_leaderboard:
        movement_index = strength_leaderboard.index(query.data)
        movement = list(STRENGTH_INLINE_BTNS.keys())[movement_index]
        movement_leaderboard = await db.strength_movements_leaderboard(movement)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(movement_leaderboard,
                                        movement,
                                        STRENGTH_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'front_squat':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[0]
        await state.set_state(StrengthData.front_squat)
        await bot.send_message(telegram_id,
                               'Введи вес фронталки в килограммах,'
                               ' например 102.5:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'back_squat':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[1]
        await state.set_state(StrengthData.back_squat)
        await bot.send_message(telegram_id,
                               'Введи вес приседа в килограммах,'
                               ' например 110.5:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'overhead_squat':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[2]
        await state.set_state(StrengthData.overhead_squat)
        await bot.send_message(telegram_id,
                               'Введи вес оверхеда в килограммах,'
                               ' например 110.5:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'push_press':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[3]
        await state.set_state(StrengthData.bench_press)
        await bot.send_message(telegram_id,
                               'Введи вес жима cтоя в килограммах,'
                               ' например 75.5:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'bench_press':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[4]
        await state.set_state(StrengthData.push_press)
        await bot.send_message(telegram_id,
                               'Введи вес жима лежа в килограммах,'
                               ' например: 60.5:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'deadlift':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[5]
        await state.set_state(StrengthData.deadlift)
        await bot.send_message(telegram_id,
                               'Введи вес становой тяги в килограммах,'
                               'например 119.6:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'clean_lift':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[6]
        await state.set_state(StrengthData.clean_lift)
        await bot.send_message(telegram_id,
                               'Введи вес тяги в толчковых углах в килограммах,'
                               'например 109.6:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'snatch_lift':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_movements_names[7]
        await state.set_state(StrengthData.snatch_lift)
        await bot.send_message(telegram_id,
                               'Введи вес тяги в рывковых углах в килограммах,'
                               'например 139.6:',
                               reply_markup=profile_keyboard_2)
        await query.answer()
    # Explosive power category
    elif query.data in power_records:
        movement_index = power_records.index(query.data)
        # getting movement name for database from dict
        movement = list(EXPLOSIVE_POWER_INLINE_BTNS.keys())[movement_index]
        # getting movement results for user
        movement_history = await db.power_movement_result_history(
            telegram_id, movement
        )
        await bot.send_message(
            telegram_id,
            text=await history_data(movement_history,
                                    movement,
                                    EXPLOSIVE_POWER_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data in power_leaderbord:
        movement_index = power_leaderbord.index(query.data)
        movement = list(EXPLOSIVE_POWER_INLINE_BTNS.keys())[movement_index]
        movement_leaderboard = await db.power_movements_leaderboard(movement)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(movement_leaderboard,
                                        movement,
                                        EXPLOSIVE_POWER_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'long_jump':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[0]
        await state.set_state(PowerData.long_jump)
        await bot.send_message(telegram_id,
                               'Введи свой прыжок в длину в сантиметрах,'
                               ' например 281.2:')
        await query.answer()
    elif query.data == 'snatch':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[1]
        await state.set_state(PowerData.snatch)
        await bot.send_message(telegram_id,
                               'Введи вес рывка с пола в сед в килограммах,'
                               ' например 82.5:')
        await query.answer()
    elif query.data == 'power_snatch':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[2]
        await state.set_state(PowerData.power_snatch)
        await bot.send_message(telegram_id,
                               'Введи вес рывка с пола в стойку в килограммах,'
                               ' например 72.5:')
    elif query.data == 'hang_snatch':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[3]
        await state.set_state(PowerData.hang_snatch)
        await bot.send_message(telegram_id,
                               'Введи вес рывка с виса в сед в килограммах,'
                               ' например 72.5:')
        await query.answer()
    elif query.data == 'hang_power_snatch':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[4]
        await state.set_state(PowerData.hang_power_snatch)
        await bot.send_message(telegram_id,
                               'Введи  вес рывка с виса в стойку в килограммах,'
                               ' например 72.5:')
        await query.answer()
    elif query.data == 'clean':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[5]
        await state.set_state(PowerData.clean)
        await bot.send_message(telegram_id,
                               'Введи вес подъема с пола на грудь в сед '
                               'в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'power_clean':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[6]
        await state.set_state(PowerData.power_clean)
        await bot.send_message(telegram_id,
                               'Введи вес подъема с пола на грудь в стойку'
                               ' в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'power_jerk':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[7]
        await state.set_state(PowerData.power_jerk)
        await bot.send_message(telegram_id,
                               'Введи вес жимового швунга'
                               ' в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'jerk':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[8]
        await state.set_state(PowerData.jerk)
        await bot.send_message(telegram_id,
                               'Введи вес толчкового швунга'
                               ' в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'split_jerk':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[9]
        await state.set_state(PowerData.split_jerk)
        await bot.send_message(telegram_id,
                               'Введи вес толчка в ножницы'
                               ' в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'thruster':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[10]
        await state.set_state(PowerData.thruster)
        await bot.send_message(telegram_id,
                               'Введи вес трастера со стоек'
                               ' в килограммах, например 72.5:')
        await query.answer()
    elif query.data == 'cluster':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = power_movement_names[11]
        await state.set_state(PowerData.cluster)
        await bot.send_message(telegram_id,
                               'Введи вес кластера'
                               ' в килограммах, например 72.5:')
        await query.answer()
    # Strength capacity category
    # --------------------------
    elif query.data in strength_cpt_records:
        # getting movement index for dict with movement names by query.data
        movement_index = strength_cpt_records.index(query.data)
        # getting movement name for database from dict
        movement = list(STRENGTH_CAPACITY_INLINE_BTNS.keys())[movement_index]
        # getting movement results for user
        movement_history = await db.strength_cpt_result_history(
            telegram_id, movement
        )
        await bot.send_message(
            telegram_id,
            text=await history_data(movement_history,
                                    movement,
                                    STRENGTH_CAPACITY_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data in strength_cpt_leaderboard:
        movement_index = strength_cpt_leaderboard.index(query.data)
        movement = list(STRENGTH_CAPACITY_INLINE_BTNS.keys())[movement_index]
        movement_leaderboard = await db.strength_cpt_movements_leaderboard(
            movement)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(movement_leaderboard,
                                        movement,
                                        STRENGTH_CAPACITY_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'deadlift_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[0]
        await state.set_state(StrengthCapacityData.deadlift)
        await bot.send_message(
            telegram_id,
            f'Вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)\n\n'
            'Введи количество повторений cтановой тяги с '
            'весом 70% от 1ПМ, например 10:')
        await query.answer()
    elif query.data == 'squat_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[1]
        await state.set_state(StrengthCapacityData.squat)
        await bot.send_message(
            telegram_id,
            f'Введи количество повторений приседа с '
            'весом 70% от 1ПМ (вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)'
            ', например 10:')
        await query.answer()
    elif query.data == 'push_press_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[2]
        await state.set_state(StrengthCapacityData.push_press)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений жима стоя с '
            'весом 70% от 1ПМ (вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)'
            ', например 10:')
        await query.answer()
    elif query.data == 'bench_press_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[3]
        await state.set_state(StrengthCapacityData.bench_press)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений жима лежа с '
            'весом 70% от 1ПМ (вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)'
            ', например 10:')
        await query.answer()
    elif query.data == 'pull_up_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[4]
        await state.set_state(StrengthCapacityData.pull_ups)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений подтягиваний с '
            'с подвесом, (вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)'
            ', например 10:')
        await query.answer()
    elif query.data == 'deeps_cpt':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = strength_cpt_movement_names[5]
        await state.set_state(StrengthCapacityData.deeps)
        await bot.send_message(
            telegram_id,
           'Введи количество повторений отжиманий'
           ' на кольцах (для мальчиков) '
           'или брусьях (для девочек)'
           'с подвесом(вес твоего снаряда - '
            f'{await weight_for_movement(telegram_id, data["movement"])} кг)'
            ', например 10:')
        await query.answer()
    # Aerobic capacity
    #----------------
    elif query.data in aerobic_capacity_records:
        movement_index = aerobic_capacity_records.index(query.data)
        movement = list(AEROBIC_CAPACITY_INLINE_BTNS.keys())[movement_index]
        movement_history = await db.aerobic_result_history(
            telegram_id, movement
        )
        await bot.send_message(
            chat_id=telegram_id,
            text=await history_data(movement_history,
                                    movement,
                                    AEROBIC_CAPACITY_INLINE_BTNS)
        )
        await query.answer()
    elif query.data in aerobic_capacity_leaderboard:
        movement_index = aerobic_capacity_leaderboard.index(query.data)
        movement = list(AEROBIC_CAPACITY_INLINE_BTNS.keys())[movement_index]
        movement_leaderboard = await db.aerobic_movements_leaderboard(movement)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(movement_leaderboard,
                                        movement,
                                        AEROBIC_CAPACITY_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == '2_km_row':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[0]
        await state.set_state(AerobicData.two_km_row)
        await bot.send_message(telegram_id,
                               'Введи время 2 км гребли'
                               ', в формате ММ:СС, например: 08:22')
        await query.answer()
    elif query.data == '5_km_row':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[1]
        await state.set_state(AerobicData.five_km_row)
        await bot.send_message(telegram_id,
                               'Введи время 5 км гребли'
                               ', в формате ММ:СС, например: 19:22')
        await query.answer()
    elif query.data == '10_km_row':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[2]
        await state.set_state(AerobicData.ten_km_row)
        await bot.send_message(telegram_id,
                               'Введи время 10 км гребли'
                               ', в формате ММ:СС или ЧЧ:ММ:СС,'
                               ' например: 01:03:22')
        await query.answer()
    elif query.data == 'row_step':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[3]
        await state.set_state(AerobicData.row_step)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'ступенчатого теста на гребле,'
                               ' например: 280')
        await query.answer()
    elif query.data == 'row_mam':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[4]
        await state.set_state(AerobicData.row_mam)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'MAM-теста на гребле,'
                               ' например: 831')
        await query.answer()
    elif query.data == 'row_1_hour':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[5]
        await state.set_state(AerobicData.one_hour_row)
        await bot.send_message(telegram_id,
                               'Введи дистанцию в метрах '
                               'за 1 час гребли,'
                               ' например: 16855')
        await query.answer()
    elif query.data == 'row_10_min':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[6]
        await state.set_state(AerobicData.ten_min_row)
        await bot.send_message(telegram_id,
                               'Введи количество калорий '
                               'за 10 минут гребли,'
                               ' например: 325')
        await query.answer()
    elif query.data == 'bike_step':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[7]
        await state.set_state(AerobicData.bike_step)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'ступенчатого теста на байке,'
                               ' например: 280')
        await query.answer()
    elif query.data == 'bike_mam':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[8]
        await state.set_state(AerobicData.bike_mam)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'MAM-теста на байке,'
                               ' например: 831')
        await query.answer()
    elif query.data == 'bike_10_min':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[9]
        await state.set_state(AerobicData.ten_min_bike)
        await bot.send_message(telegram_id,
                               'Введи количество калорий '
                               'за 10 минут байка,'
                               ' например: 325')
        await query.answer()
    elif query.data == 'skierg_step':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[10]
        await state.set_state(AerobicData.skierg_step)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'ступенчатого теста на скиэрге (лыжах),'
                               ' например: 280')
        await query.answer()
    elif query.data == 'skierg_mam':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[11]
        await state.set_state(AerobicData.bike_mam)
        await bot.send_message(telegram_id,
                               'Введи максимальные ватты '
                               'MAM-теста на скиэрге (лыжах),'
                               ' например: 831')
        await query.answer()
    elif query.data == 'skierg_10_min':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = aerobic_movement_names[12]
        await state.set_state(AerobicData.ten_min_bike)
        await bot.send_message(telegram_id,
                               'Введи количество калорий '
                               'за 10 минут cкиерга (лыж),'
                               ' например: 325')
        await query.answer()
    # gymnastics category
    # -------------------
    elif query.data in gymnastics_records:
        movement_index = gymnastics_records.index(query.data)
        # getting movement name for database from dict
        movement = list(GYMNASTICS_INLINE_BTNS.keys())[movement_index]
        # getting movement results for user
        movement_history = await db.gymnastics_result_history(
            telegram_id, movement
        )
        await bot.send_message(
            telegram_id,
            text=await history_data(movement_history,
                                    movement,
                                    GYMNASTICS_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data in gymnastics_leaderboard:
        movement_index = gymnastics_leaderboard.index(query.data)
        movement = list(GYMNASTICS_INLINE_BTNS.keys())[movement_index]
        movement_leaderboard = await db.gymnastics_movements_leaderboard(
            movement)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(movement_leaderboard,
                                        movement,
                                        GYMNASTICS_INLINE_BTNS),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == 'pull_up_1_rm':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[0]
        await state.set_state(GymnasticsData.pull_up_one_rm)
        await bot.send_message(telegram_id,
                               'Введи вес подвеса 1ПМ строгого подтягивания'
                               ' в килограммах,'
                               ' например: 45.5')
        await query.answer()
    elif query.data == 'ring_deep_1_rm':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[1]
        await state.set_state(GymnasticsData.ring_deep_one_rm)
        await bot.send_message(telegram_id,
                               'Введи вес подвеса 1ПМ строгого отжимания'
                               'на кольцах в килограммах,'
                               ' например: 52.5')
        await query.answer()
    elif query.data == 'deep_1rm':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[2]
        await state.set_state(GymnasticsData.deep_one_rm)
        await bot.send_message(telegram_id,
                               'Введи вес подвеса 1ПМ строгого отжимания'
                               'на брусьях в килограммах,'
                               ' например: 52.6')
        await query.answer()
    elif query.data == 'pull_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[3]
        await state.set_state(GymnasticsData.deep_one_rm)
        await bot.send_message(telegram_id,
                               'Введи количество подтягиваний за 1 подход,'
                               ' например: 22')
    elif query.data == 'strict_hs_push_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[4]
        await state.set_state(GymnasticsData.strict_hs_push_ups)
        await bot.send_message(telegram_id,
                               'Введи количество строгих отжиманий в стойке'
                               ' за 1 подход,'
                               ' например: 22')
    elif query.data == 'hs_push_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[5]
        await state.set_state(GymnasticsData.strict_hs_push_ups)
        await bot.send_message(telegram_id,
                               'Введи количество отжиманий в стойке кипом'
                               ' за 1 подход,'
                               ' например: 32')
    elif query.data == 'strict_ring_muscle_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[6]
        await state.set_state(GymnasticsData.strict_ring_muscle_ups)
        await bot.send_message(telegram_id,
                               'Введи количество cтрогих выходов на кольцах'
                               ' за 1 подход,'
                               ' например: 11')
    elif query.data == 'ring_muscle_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[7]
        await state.set_state(GymnasticsData.strict_ring_muscle_ups)
        await bot.send_message(telegram_id,
                               'Введи количество выходов на кольцах'
                               ' за 1 подход,'
                               ' например: 14')
    elif query.data == '90_sec_ring_muscle_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[8]
        await state.set_state(GymnasticsData.time_ring_muscle_ups)
        await bot.send_message(telegram_id,
                               'Введи количество выходов на кольцах'
                               ' за 90 секунд,'
                               ' например: 22')
    elif query.data == 'muscle_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[9]
        await state.set_state(GymnasticsData.muscle_ups)
        await bot.send_message(telegram_id,
                               'Введи количество выходов на перекладине'
                               ' за 1 подход,'
                               ' например: 22')
    elif query.data == '90_sec_muscle_ups':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[10]
        await state.set_state(GymnasticsData.time_muscle_ups)
        await bot.send_message(telegram_id,
                               'Введи количество выходов на перекладине'
                               ' за 90 секунд,'
                               ' например: 22')
    elif query.data == 't2b':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[11]
        await state.set_state(GymnasticsData.toes_to_bar)
        await bot.send_message(telegram_id,
                               'Введи количество НКП (ног к перекладине)'
                               ' за 1 подход,'
                               ' например: 33')
    elif query.data == 'ropes':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[12]
        await state.set_state(GymnasticsData.ropes)
        await bot.send_message(telegram_id,
                               'Введи количество канатов 4.5 метра с ногами'
                               ' за 2 минуты,'
                               ' например: 10')
    elif query.data == 'legless_ropes':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[13]
        await state.set_state(GymnasticsData.legless_ropes)
        await bot.send_message(telegram_id,
                               'Введи количество канатов 4.5 метра без ног'
                               ' за 2 минуты,'
                               ' например: 10')
    elif query.data == 'l_sit':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[14]
        await state.set_state(GymnasticsData.l_sit)
        await bot.send_message(telegram_id,
                               'Введи количество cекунд удержания уголка'
                               ' в упоре на полу за 1 подход,'
                               ' например: 40')
    elif query.data == 'hang_l_sit':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[15]
        await state.set_state(GymnasticsData.hang_l_sit)
        await bot.send_message(telegram_id,
                               'Введи количество cекунд удержания уголка'
                               ' в висе на перекладине за 1 подход,'
                               ' например: 40')
    elif query.data == 'hang':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[16]
        await state.set_state(GymnasticsData.hang)
        await bot.send_message(telegram_id,
                               'Введи количество cекунд'
                               ' в висе на перекладине за 1 подход,'
                               ' например: 62')
    elif query.data == 'hs_walk':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[17]
        await state.set_state(GymnasticsData.hs_walk)
        await bot.send_message(telegram_id,
                               'Введи количество метров ходьбы на руках'
                               ' за 1 подход без падений,'
                               ' например: 40')
    elif query.data == 'min_hs_walk':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['movement'] = gymnastics_movement_names[18]
        await state.set_state(GymnasticsData.time_hs_walk)
        await bot.send_message(telegram_id,
                               'Введи количество метров ходьбы на руках'
                               ' за 1 минуту,'
                               ' например: 25')
    elif query.data in metcon_records:
        metcon_index = metcon_records.index(query.data)
        # getting movement name for database from dict
        metcon = list(METCONS_INLINE_KB.keys())[metcon_index]
        # getting movement results for user
        metcon_history = await db.metcon_result_history(
            telegram_id, metcon
        )
        await bot.send_message(
            telegram_id,
            text=await history_data(metcon_history,
                                    metcon,
                                    METCONS_INLINE_KB),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data in metcon_leaderbord:
        metcon_index = metcon_leaderbord.index(query.data)
        # getting movement name for database from dict
        metcon = list(METCONS_INLINE_KB.keys())[metcon_index]
        # getting movement results for user
        metcon_leaderboard = await db.metcon_leaderboard(metcon)
        await bot.send_message(
            telegram_id,
            text=await leaderboard_data(metcon_leaderboard,
                                        metcon,
                                        METCONS_INLINE_KB),
            reply_markup=profile_keyboard_2)
        await query.answer()
    elif query.data == '150_burpees':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[0]
        await state.set_state(MetconsData.hundred_burpees)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ММ:СС, например 13:22'
        )
        await query.answer()
    elif query.data == '150_burpees_desc':
        await bot.send_message(
            telegram_id,
            'Выполнить как можно быстрее 150 бурпей с прыжком +15см в высоту.\n'
            'Для удобства найти перекладину которая на 15 см'
            ' выше ладони вытянутой руки'
        )
        await query.answer()
    elif query.data == 'karen':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[1]
        await state.set_state(MetconsData.karen)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ММ:СС, например 13:22'
        )
        await query.answer()
    elif query.data == 'karen_desc':
        await bot.send_message(
            telegram_id,
            'Карен:\n\n'
            'Выполнить как можно быстрее 150 бросков мяча'
        )
        await query.answer()
    elif query.data == 'murph':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[2]
        await state.set_state(MetconsData.murph)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ЧЧ:ММ:СС, '
            'например 02:13:22'
        )
        await query.answer()
    elif query.data == 'murph_desc':
        await bot.send_message(
            telegram_id,
            'Мёрф \n\n'
            'На время:\n'
            '1600 метров бег\n'
            '100 подтягиваний\n'
            '200 отжиманий\n'
            '300 приседаний\n'
            '1600 метров бег\n\n'
            'В Rх версии комплекс выполняется с жилетом 9 кг для мужчин и '
            '6 кг для девушек.\n'
            'В Scaled версии - без жилета'
        )
        await query.answer()
    elif query.data == 'cindy':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[3]
        await state.set_state(MetconsData.cindy)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений, '
            'например 98'
        )
        await query.answer()
    elif query.data == 'cindy_desc':
        await bot.send_message(
            telegram_id,
            'Cинди \n\n'
            'AMRAP 20 минут\n'
            '5 подтягиваний\n'
            '10 отжиманий\n'
            '15 приседаний\n\n'
            'Для самых мощных - выполнять в жилете 9 кг.'
        )
        await query.answer()
    elif query.data == 'linda':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[4]
        await state.set_state(MetconsData.linda)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ММ:СС, например 13:22'
        )
        await query.answer()
    elif query.data == 'linda_desc':
        user_weight = list(await db.get_user_biometrics(telegram_id))[3]
        await bot.send_message(
            telegram_id,
            f'Линда \n\n'
            f'Выполнить за минимальное время\n'
            f'10-9-8-7-6-5-4-3-2-1 повторений,\n'
            f'Cтановая тяга {user_weight * 1.5} кг (1.5 веса тела) \n'
            f'Жим лежа {user_weight} кг (вес тела) \n'
            f'Взятие в сед {user_weight * 0.75} кг (3/4 веса тела)\n\n'
            f'Выполняется как обратная лесенка:\n'
            f'10 cтановых, 10 жимов, 10 взятий, 9 становых, 9 жимов, 9 взятий'
            f'и так далее'
        )
        await query.answer()
    elif query.data == 'open_13_1':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[5]
        await state.set_state(MetconsData.open_13_1)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений, '
            'например 98'
        )
        await query.answer()
    elif query.data == 'open_13_1_desc':
        await bot.send_message(
            telegram_id,
            'Open 13.1\n\n'
            'AMRAP 17 минут:\n'
            '40 берпи\n'
            '30 рывков (35/20 кг)\n'
            '30 берпи\n'
            '30 рывков (60/35 кг)\n'
            '20 берпи\n'
            '30 рывков (75/45 кг)\n'
            '10 берпи'
            'максимальное количество рывков (95/55 кг) за оставшееся время'
        )
        await query.answer()
    elif query.data == 'kalsu':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[6]
        await state.set_state(MetconsData.kalsu)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ЧЧ:ММ:СС, '
            'например 02:13:22'
        )
        await query.answer()
    elif query.data == 'kalsu_desc':
        await bot.send_message(
            telegram_id,
            'Калсу\n\n'
            'На время:\n'
            '100 трастеров 60/43 кг \n'
            'При этом каждую минуту начинаем с 5 берпи, включая первую минуту'
        )
        await query.answer()
    elif query.data == 'open_19_1':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[7]
        await state.set_state(MetconsData.open_19_1)
        await bot.send_message(
            telegram_id,
            'Введи количество повторений, например 122'
        )
        await query.answer()
    elif query.data == 'open_19_1_desc':
        await bot.send_message(
            telegram_id,
            'Open 19.1\n\n'
            'AMRAP 15 минут:\n'
            '19 бросков мяча\n19 калорий гребли\n'
        )
        await query.answer()
    elif query.data == 'open_16_5':
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['metcon'] = metcon_names[8]
        await state.set_state(MetconsData.open_16_5)
        await bot.send_message(
            telegram_id,
            'Введи время выполнения комплекса в формате ММ:СС, например 13:22'
        )
        await query.answer()
    elif query.data == 'open_16_5_desc':
        await bot.send_message(
            telegram_id,
            'Open 16.5\n\n'
            'На время:\n'
            '21-18-15-12-9-6-3\n'
            'Трастеры 43/30 кг\n'
            'Фронтальные берпи через штангу\n'
        )
        await query.answer()


def register_profile_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(choose_category,
                                       state=MainMenu.profile)
