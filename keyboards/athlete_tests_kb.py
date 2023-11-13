from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import db

# begins from 0 - 1st day, 21 - last day
REST_DAYS: list = [2, 5, 6, 8]
REMAKE_DAYS: list = [12, 13]
# amount of days in 2 test weeks
TEST_DAYS: int = 14
DAYS_IN_WEEK: int = 7


def _create_week(inline_keyboard: InlineKeyboardMarkup, start_day: int):
    """
    Helper function that creates buttons for a week.
    """
    for day in range(start_day, start_day + 7):
        if day in REST_DAYS:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    text=f'🏝️',
                    callback_data=str(day + 1)
                )
            )
        elif day in REMAKE_DAYS:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    text=f'🔁',
                    callback_data=str(day + 1)
                )
            )
        else:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    text=f'{day + 1}',
                    callback_data=str(day + 1)
                )
            )


async def tests_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Creates inline keyboard for workout tests.
    """
    inline_keyboard = InlineKeyboardMarkup(row_width=7)

    inline_keyboard.row()
    inline_keyboard.insert(InlineKeyboardButton(f'Тестовые дни',
                                                callback_data='ignore_callback'))
    # test week 1
    inline_keyboard.row()
    _create_week(inline_keyboard, 0)
    # test week 2
    inline_keyboard.row()
    _create_week(inline_keyboard, 7)
    # test week 3
    inline_keyboard.row()
    _create_week(inline_keyboard, 13)

    return inline_keyboard
