from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# begins from 0 - 1st day, 21 - last day
REST_DAYS: list = [4, 7, 9, 14, 17, 20, 21]
REMAKE_DAYS: list = [18, 19]


def _create_week(inline_keyboard: InlineKeyboardMarkup, start_day: int):
    """
    Helper function that creates buttons for a week.
    """
    for day in range(start_day, start_day + 7):
        if day in REST_DAYS:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    text=f'🏝️',
                    callback_data=str(day)
                )
            )
            continue
        if day in REMAKE_DAYS:
            inline_keyboard.insert(
                InlineKeyboardButton(
                    text=f'🔁',
                    callback_data=str(day)
                )
            )
            continue
        inline_keyboard.insert(
            InlineKeyboardButton(
                text=f'{day}',
                callback_data=str(day)
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
    _create_week(inline_keyboard, 1)
    # test week 2
    inline_keyboard.row()
    _create_week(inline_keyboard, 8)
    # test week 3
    inline_keyboard.row()
    _create_week(inline_keyboard, 15)
    return inline_keyboard
