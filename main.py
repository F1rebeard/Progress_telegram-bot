import logging
import asyncio
import aioschedule

from aiogram import executor

from create_bot import dp
from handlers import (users,
                      admin, registration,
                      payment, biometrics,
                      strength, profile, power, strength_capacity,
                      aerobic_capacity, gymnastics, metcons, freeze)
from handlers.payment import subscription_warnings
from handlers.freeze import freeze_warnings
from handlers.admin import send_birthday_users
from handlers.users import start_poll_for_time_in_progress
from workout_clr import workout_calendar

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    force=True)

users.register_users_handlers(dp)
payment.register_payment_handlers(dp)
registration.register_registration_handlers(dp)
admin.register_admin_handlers(dp)
freeze.register_freeze_handlers(dp)
gymnastics.register_gymnastics_handlers(dp)
strength_capacity.register_strength_capacity_handlers(dp)
aerobic_capacity.register_aerobic_handelrs(dp)
power.register_power_handlers(dp)
strength.register_strength_handlers(dp)
biometrics.register_biometrics_handlers(dp)
metcons.register_metcon_handlers(dp)
profile.register_profile_handlers(dp)
workout_calendar.register_workout_handelrs(dp)


async def scheduler():
    aioschedule.every(90).seconds.do(start_poll_for_time_in_progress)
    aioschedule.every(24).hours.do(subscription_warnings)
    aioschedule.every(24).hours.do(freeze_warnings)
    aioschedule.every(1).day.at("15:00").do(send_birthday_users)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    asyncio.create_task(scheduler())
    print('Bot is online!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
