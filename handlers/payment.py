import logging
import os

from aiogram import types
from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from datetime import datetime
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from create_bot import bot, db
from config.constants import ADMIN_IDS
from keyboards.user_kb import (choose_sub,
                               registration_button,
                               subscription_kb,
                               user_keyboard,
                               unfreeze_kb)
from handlers.registration import Registration

load_dotenv()

PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')

# 1 месяц без куратора
standard_price = [
    types.LabeledPrice(label='30 дней без куратора',
                       amount=300000),
]

# 1 месяц с куратором
plus_coach_price = [
    types.LabeledPrice(label='30 дней c куратором',
                       amount=500000),
]


class PaymentStatus(StatesGroup):
    Choose = State()


async def choose_subscription(message: types.Message, state: FSMContext):
    if message.chat.type == 'private':
        await state.set_state(PaymentStatus.Choose)
        await bot.send_message(
            message.from_user.id,
            'Выбери тип подписки:',
            reply_markup=choose_sub
        )


async def pay_for_subscription(query: types.CallbackQuery, state: FSMContext):
    telegram_id = query.from_user.id
    await bot.delete_message(telegram_id, query.message.message_id)
    if query.data == 'one_month_sub':
        await bot.send_invoice(
            chat_id=telegram_id,
            title='30 дней подписки на "Прогресс"',
            description='Открывает доступ к боту с тренировками, '
                        'результатами, тестами и упражнениями на 30 дней '
                        'без куратора',
            need_email=True,
            send_email_to_provider=True,
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency='rub',
            prices=standard_price,
            start_parameter='standard_sub',
            payload='standard_thirty_days_sub',
            is_flexible=False,
            provider_data={
                "receipt": {
                    "items": [
                        {
                            "description": "Подписка на 30 дней без куратора",
                            "quantity": "1.00",
                            "amount": {
                                "value": "3000.00",
                                "currency": "RUB"
                            },
                            "vat_code": 1,
                        }
                    ],
                },
                "capture": True,
            }
            )
        await state.finish()
        await query.answer()
    if query.data == 'one_month_sub_plus':
        await bot.send_invoice(
            chat_id=query.from_user.id,
            title='30 дней подписки на "Прогресс" c куратором',
            description='Открывает доступ к боту с тренировками, '
                        'результатами, тестами и упражнениями на 30 дней '
                        'с куратором',
            need_name=True,
            send_email_to_provider=True,
            provider_token=PAYMENT_PROVIDER_TOKEN,
            currency='rub',
            prices=plus_coach_price,
            start_parameter='plus_coach_sub',
            payload='plus_coach_thirty_days_sub',
            is_flexible=False,
            provider_data={
                "receipt": {
                    "items": [
                        {
                            "description": "Подписка на 30 дней c куратором",
                            "quantity": "1.00",
                            "amount": {
                                "value": "5000.00",
                                "currency": "RUB"
                            },
                            "vat_code": 1,
                        }
                    ],
                },
                "capture": True,
            }
        )
        await state.finish()
        await query.answer()


async def subscription_pre_checkout(
        pre_checkout_query: types.PreCheckoutQuery,
        state: FSMContext):
    if not hasattr(pre_checkout_query.order_info, 'email'):
        return await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message='Email не указан'
        )
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message='Не получены данные об оплате'
    )
    await state.set_state(Registration.payment)


async def got_payment(message: types.Message, state: FSMContext):
    """

    :param message:sqlite_master
    :param state:
    :return:
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    if await db.user_exists(telegram_id):
        # добавляет подписку +30 дней
        await db.update_user_subscription(telegram_id)
        # проверяет статус подписки
        if not await db.check_subscription_status(telegram_id):
            # если статус отрицательный, активирует статус
            await db.activate_subscription_status(telegram_id)
        subscription_date = await db.get_user_subscription_date(telegram_id)
        subscription_date = subscription_date.strftime("%d.%m.%Y")
        user_name = await db.get_user_name(telegram_id)
        await state.finish()
        if message.successful_payment.invoice_payload == 'standard_thirty_days_sub':
            await bot.send_message(
                telegram_id,
                f'Оплата прошла успешно 👍\n\n'
                f'Твоя подписка действует до {subscription_date}',
                reply_markup=user_keyboard)
            for admin_id in ADMIN_IDS:
                # [0] - имя [1] - фамилия
                try:
                    await bot.send_message(
                        admin_id,
                        f'{user_name[0]} {user_name[1]} оплатил(а) подписку '
                        f'(без куратора) 🤑🤑🤑\n'
                        f'telegram_id: {telegram_id}\n'
                        f'username: @{username}\n\n'
                    )
                except ChatNotFound:
                    logging.info('Чат не найден!')
                continue
        elif message.successful_payment.invoice_payload == 'plus_coach_thirty_days_sub':
            await bot.send_message(
                telegram_id,
                f'Оплата прошла успешно👍\n\n '
                f'Твоя подписка c куратором действует '
                f'до {subscription_date} \n\n'
                f'Для назначения куратора свяжись с @uncle_boris',
                reply_markup=user_keyboard)
            for admin_id in ADMIN_IDS:
                # [0] - имя [1] - фамилия
                await bot.send_message(
                    admin_id,
                    f'{user_name[0]} {user_name[1]} оплатил(а) подписку '
                    f'(с куратором) 🤑🤑🤑\n'
                    f'telegram_id: {telegram_id}\n'
                    f'username: @{username}\n\n'
                )
    else:
        async with state.proxy() as data:
            data['telegram_id'] = telegram_id
            data['username'] = message.from_user.username
            data['registration_date'] = datetime.now().date()
        await db.add_user(state)
        await db.new_user_subscription(telegram_id)
        await db.activate_subscription_status(telegram_id)
        subscription_date = await db.get_user_subscription_date(telegram_id)
        subscription_date = subscription_date.strftime("%d.%m.%Y")
        await state.set_state(Registration.new_user)
        if message.successful_payment.invoice_payload == 'standard_thirty_days_sub':
            await bot.send_message(
                telegram_id,
                f'Оплата прошла успешно 👍\n\n'
                f'Твоя подписка действует до {subscription_date}\n\n'
                f'А теперь нужно закончить регистрацию, это займет буквально '
                f'пару минут.\n',
                reply_markup=registration_button
            )
            for admin_id in ADMIN_IDS:
                # [0] - имя [1] - фамилия
                await bot.send_message(
                    admin_id,
                    f'К нам присоединился(-ась) @{username}\n\n '
                    f'(без куратора) 🤑🤸\n'
                    f'telegram_id: {telegram_id}\n'
                )
        elif message.successful_payment.invoice_payload == 'plus_coach_thirty_days_sub':
            await bot.send_message(
                telegram_id,
                f'Оплата прошла успешно👍\n\n '
                f'Твоя подписка c куратором действует до '
                f'до {subscription_date}\n\n'
                f'Для назначения куратора свяжись с @uncle_boris \n\n'
                f'А теперь нужно закончить регистрацию, это займет буквально '
                f'пару минут.\n',
                reply_markup=registration_button)
            for admin_id in ADMIN_IDS:
                # [0] - имя [1] - фамилия
                await bot.send_message(
                    admin_id,
                    f'К нам присоединился(-ась) @{username}\n\n '
                    f'(с куратором) 🤑🤸\n'
                    f'telegram_id: {telegram_id}\n'
                )


async def subscription_warnings():
    """
    A Functions which checks and warns user about end of subscription
    :return:
    """
    try:
        today = datetime.now().date()
        users_subs = await db.get_users_subscription_date()
        # у кого закончилась подписка
        ended = []
        # заканчивается сегодня
        ending_today = []
        # заканчивается завтра
        ending_tomorrow = []
        # заканчивается через два дня
        ending_in_two_days = []
        for data in users_subs:
            # data[1] = subscription date
            # data[0] = telegram_id
            subscription_date = datetime.strptime(data[1], "%Y-%m-%d").date()
            if (subscription_date - today).days == 0:
                ending_today.append(data[0])
            elif (subscription_date - today).days == 1:
                ending_tomorrow.append(data[0])
            elif (subscription_date - today).days == 2:
                ending_in_two_days.append(data[0])
            elif (subscription_date - today).days < 0:
                if await db.check_subscription_status(telegram_id=data[0]):
                    await db.deactivate_subscription_status(telegram_id=data[0])
                    ended.append(data[0])
                else:
                    pass
        for telegram_id in ended:
            try:
                await bot.send_message(
                    telegram_id,
                    'Твоя подписка закончилась 😬😭, скорее возвращайся!',
                    reply_markup=subscription_kb
                )
            except ChatNotFound or BotBlocked:
                logging.info('Нету чата с этим пользователем')
            continue
        for telegram_id in ending_today:
            try:
                await bot.send_message(telegram_id,
                                       'Твоя подписка заканчивается сегодня!\n\n'
                                       'Не забудь продлить 🤖')
            except ChatNotFound:
                logging.info('Нету чата с этим пользователем')
            continue
        for telegram_id in ending_tomorrow:
            try:
                await bot.send_message(telegram_id,
                                       'Твоя подписка заканчивается завтра!\n\n'
                                       'Не забудь продлить 🤖')
            except ChatNotFound or BotBlocked:
                logging.info('Нету чата с этим пользователем')
            continue
        for telegram_id in ending_in_two_days:
            try:
                await bot.send_message(telegram_id,
                                       'Твоя подписка заканчивается'
                                       ' послезавтра!\n\n'
                                       'Не забудь продлить 🤖'
                                       )
            except ChatNotFound or BotBlocked:
                logging.info('Нету чата с этим пользователем')
            continue
    except ValueError or TypeError:
        logging.info('Нет данных о подписке!')


async def subscription_control(telegram_id: int):
    """
    :param telegram_id:
    :return:
    """
    # запрашиваем статус подписки
    sub_status = await db.check_subscription_status(telegram_id)
    freeze_status = await db.check_freeze_status(telegram_id)
    if not sub_status:
    # если статус подписки отрицательный
    # то выводим сообщение о подписке
        chat = await bot.get_chat(telegram_id)
        await bot.send_message(chat_id=chat.id,
                               text='Твоя подписка закончилась 😞',
                               reply_markup=subscription_kb)
    elif freeze_status:
        chat = await bot.get_chat(telegram_id)
        await bot.send_message(chat_id=chat.id,
                               text='Твоя подписка заморожена ⛄',
                               reply_markup=unfreeze_kb)
    else:
        pass


def register_payment_handlers(dp: Dispatcher):
    dp.register_pre_checkout_query_handler(
        subscription_pre_checkout,
        lambda query: True
    )
    dp.register_message_handler(
        choose_subscription,
        text='⏳🈂 Подписка',
        state='*'
    )
    dp.register_callback_query_handler(
        pay_for_subscription,
        lambda query: True,
        state=PaymentStatus.Choose
    )
    dp.register_message_handler(
        got_payment,
        content_types=ContentType.SUCCESSFUL_PAYMENT,
        state=Registration.payment
    )
