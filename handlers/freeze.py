import logging
import os

from datetime import datetime
from dotenv import load_dotenv
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import bot, db
from handlers.admin import UsersInfo
from keyboards.admin_kb import yes_or_no_inline_kb, admin_tools
from keyboards.user_kb import unfreeze_kb, user_keyboard

load_dotenv()

ADMIN_IDS = os.getenv('ADMIN_IDS')


async def freezing_subscription_approval(message: types.Message,
                                         state: FSMContext):
    """
    Approving or not freezing using subs with selected amount of days.
    :param message:
    :param state:
    :return:
    """
    if message.from_user.id in ADMIN_IDS:
        try:
            async with state.proxy() as info:
                info['freeze_days'] = int(message.text)
            if info['freeze_days'] <= 0:
                await message.answer(
                    'Введи положительное целое число дней!'
                )
            else:
                await message.answer(
                    f'Заморозить подписку для @{info["nickname"]} '
                    f'на {info["freeze_days"]} дней(я)?',
                    reply_markup=yes_or_no_inline_kb
                )
        except TypeError or ValueError:
            return logging.info('Неверный формат данных в сообщении!')


async def freeze_subscription(query: types.CallbackQuery,
                              state: FSMContext):
    """

    :param query:
    :param state:
    :return:
    """
    async with state.proxy() as info:
        if query.data == 'yes_action':
            # устанавливаем дату то которой подписка заморожена
            await db.freeze_user_subscription(
                telegram_id=int(info['user_id']),
                freeze_days=info['freeze_days']
            )
            # включаем статус заморозки для пользователя
            await db.activate_freeze_status(
                telegram_id=int(info['user_id'])
            )
            # добавляем количество дней заморозки к дате окончания подписки
            await db.add_user_subscription(
                telegram_id=int(info['user_id']),
                days=str(info['freeze_days'])
            )
            # отправляем сообщение пользователю о заморозке подписки
            await bot.send_message(
                chat_id=info['user_id'],
                text=f'Твоя подписка заморожена ❄️'
                     f' на {info["freeze_days"]} дней(я). Для разморозки '
                     f'раньше воспользуйся кнопкой ниже.\n\n'
                     f'На период заморозки тренировки недоступны 🥶',
                reply_markup=unfreeze_kb
            )
            # отправляем сообщение админу об успешной заморозке
            await bot.edit_message_text(
                f'Подписка для @{info["nickname"]} заморожена!',
                message_id=query.message.message_id,
                chat_id=query.message.chat.id
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


async def unfreeze_subscription_approval(message: types.Message,
                                         state: FSMContext):
    """
    Asking user for unfreezing the subscription.
    :param message:
    :param state:
    :return:
    """
    await state.set_state(UsersInfo.unfreeze_subscription)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Разморозить подписку заранее?',
        reply_markup=yes_or_no_inline_kb
    )


async def unfreeze_subscription(query: types.CallbackQuery,
                                state: FSMContext):
    """

    :param query:
    :param state:
    :return:
    """
    telegram_id = query.from_user.id
    if query.data == 'yes_action':
        # выключаем статус заморозки у пользователя
        await db.deactivate_freeze_status(telegram_id)
        # отменяем допольнительное смещенее даты подписки
        # на количество неиспользованных дней в текущей заморозке
        await db.decrease_user_subscription(telegram_id)
        # удаляем дату "до" текущей заморозки
        await db.clear_frozen_till_data(telegram_id)
        # сообщаем об отмене, включаем меню
        await query.message.answer('Заморозка отменена, '
                                   'возвращаемся к тренировкам 🏋🏻',
                                   reply_markup=user_keyboard)
        await query.answer()
    elif query.data == 'no_action':
        current_state = await state.get_state()
        if current_state is None:
            return
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await query.message.answer('Отменил', reply_markup=admin_tools)
        await query.answer()


async def freeze_warnings():
    """
    Checks freeze dates and statuses of users and automatically
    ends freezing time.
    :return:
    """
    try:
        today = datetime.now().date()
        users_freeze_dates = await db.get_users_frozen_till_dates()
        ended = []
        ending_today = []
        for data in users_freeze_dates:
            # data[0] - telegram_id
            # data[1] - frozen_till date
            frozen_till_dates = datetime.strptime(data[1], "%Y-%m-%d").date()
            if (frozen_till_dates - today).days == 0:
                ending_today.append(data[0])
            elif (frozen_till_dates - today).days < 0:
                if await db.check_freeze_status(telegram_id=data[0]):
                    await db.deactivate_freeze_status(telegram_id=data[0])
                    await db.clear_frozen_till_data(telegram_id=data[0])
                    ended.append(data[0])
                else:
                    pass
        for telegram_id in ended:
            await bot.send_message(
                telegram_id,
                'Твоя заморозка закончилась, '
                'возвращаемся к тренировкам 🏋🏻',
                reply_markup=user_keyboard
            )
        for telegram_id in ending_today:
            await bot.send_message(
                telegram_id,
                'Сегодня последний день заморозки, '
                'завтра твоя подписка станет активна 🤖'
            )
    except ValueError or TypeError:
        logging.info('Нет данных о заморозке!')


def register_freeze_handlers(dp: Dispatcher):
    """
    Registration of freeze action handlers
    :param dp:
    :return:
    """
    dp.register_callback_query_handler(freeze_subscription,
                                       lambda query: True,
                                       state=UsersInfo.freeze_subscription)
    dp.register_callback_query_handler(unfreeze_subscription,
                                       lambda query: True,
                                       state=UsersInfo.unfreeze_subscription)
    dp.register_message_handler(freezing_subscription_approval,
                                state=UsersInfo.freeze_subscription)
    dp.register_message_handler(unfreeze_subscription_approval,
                                text='❄️ Разморозка',
                                state='*')