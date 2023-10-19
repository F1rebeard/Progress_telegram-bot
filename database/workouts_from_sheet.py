import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

from create_bot import db



# 0 - Первый уровень
# 1 - Второй уровень
# 2 - Минкайфа
# 3 - Новосиб
WORKSHEETS = {
    0: 'Первый',
    1: 'Второй',
    2: 'Минкайфа',
    3: 'Соревнования'
}


def get_dates_ranges_from_cell(cell_value: str) -> list:
    """
    Gets a list of dates between ranges given in string from cell.
    :param cell_value:
    :return:
    """
    start, end = cell_value.split('-')

    # текущий год
    current_year = datetime.now().year
    # получаем начальную и конечную дату
    start_date = datetime.strptime(f'{start}.{current_year}', '%d.%m.%Y')
    end_date = datetime.strptime(f'{end}.{current_year}', '%d.%m.%Y')

    # Ensure end date is always after start date
    if end_date < start_date:
        end_date = end_date.replace(year=end_date.year + 1)

    # Generate the range of dates
    date_range = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d')
                  for x in range((end_date - start_date).days + 1)]
    return date_range


def get_week_workouts(worksheet_id: int, sheet: gspread.Spreadsheet):
    """
    Получаем последнюю неделю тренировок из гугл-таблицы.
    :param worksheet_id:
    :param sheet:
    :return:
    """
    # открываем лист в гугл таблице
    worksheet = sheet.get_worksheet(worksheet_id)
    # значение в первой колонке с датами
    col_values = worksheet.col_values(1)
    # получаем последний ряд с данными
    last_row = worksheet.row_values(len(col_values))
    return last_row


async def delete_workouts_from_database(
        sheet_title: str,
        json_path: str
):
    """

    :param sheet_title:
    :param json_path:
    :return:
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path,
                                                                   scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_title)
    #берём лист с тренировками первого уровня
    worksheet_id = 0
    last_row = get_week_workouts(worksheet_id, sheet)
    last_dates = get_dates_ranges_from_cell(last_row[0])
    await db.delete_last_workouts(last_dates)


async def get_data_from_google_sheet(
        sheet_title: str,
        json_path: str
):
    """

    :param sheet_title:
    :param json_path:
    :return:
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path,
                                                                   scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_title)

    for worksheet_id in list(WORKSHEETS.keys()):
        workouts_level = WORKSHEETS.get(worksheet_id)
        last_row = get_week_workouts(worksheet_id, sheet)
        last_dates = get_dates_ranges_from_cell(last_row[0])
        workouts = last_row[2:]
        final_list = [
            [date, workout, workouts_level] for date, workout in zip(
                last_dates, workouts
            ) if workout
        ]
        for week_workouts in final_list:
            await db.upload_new_workouts(week_workouts)
