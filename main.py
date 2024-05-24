import logging
import asyncio
import aioschedule

from aiogram import executor

from create_bot import dp
from handlers import (users,
                      admin, registration,
                      payment, biometrics, questions,
                      strength, profile, power, strength_capacity,
                      aerobic_capacity, gymnastics, metcons, freeze)
from handlers.payment import subscription_warnings
from handlers.freeze import freeze_warnings
from handlers.admin import send_birthday_users, backup_database
from handlers.questions import (start_questions_about_workout_week,
                                start_poll_for_time_in_progress)
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
questions.register_question_handlers(dp)
workout_calendar.register_workout_handelrs(dp)


async def scheduler():
    aioschedule.every(1).day.at("09:15").do(backup_database)
    aioschedule.every(1).day.at("15:00").do(send_birthday_users)
    aioschedule.every(1).day.at("18:15").do(subscription_warnings)
    aioschedule.every(1).day.at("18:15").do(freeze_warnings)
    aioschedule.every(1).day.at("20:10").do(start_poll_for_time_in_progress)
    aioschedule.every(1).day.at("20:30").do(start_poll_for_time_in_progress)

    # Schedule the task to run on Saturdays
    aioschedule.every().saturday.at("11:10").do(
        start_questions_about_workout_week)
    aioschedule.every().saturday.at("16:10").do(
        start_questions_about_workout_week)
    aioschedule.every().saturday.at("20:45").do(
        start_questions_about_workout_week)

    # Schedule the task to run on Sundays
    aioschedule.every().sunday.at("11:10").do(
        start_questions_about_workout_week)
    aioschedule.every().sunday.at("16:10").do(
        start_questions_about_workout_week)
    aioschedule.every().sunday.at("20:45").do(
        start_questions_about_workout_week)

    while True:
        await asyncio.sleep(1)
        await aioschedule.run_pending()


async def on_startup(_):
    await asyncio.create_task(scheduler())
    logging.info('Bot is ONLINE!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
