import logging
import locale

from datetime import date, datetime, timedelta
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import mplcyberpunk

from create_bot import db


async def characteristics_graphic(values: list, telegram_id: int):
    """
    :param telegram_id:
    :param values:
    :return:
    """
    # Название осей для исследумых параметров
    labels = [
        'Сила',
        'Взрывная\n сила',
        'Силовая\n выносливость',
        'Выносливость,\nэргометры',
        'Гимнастика',
        'Метконы',
    ]
    # user_info[0] - имя
    # user_info[1] - фамилия
    # user_info[2] - уровень
    user_info = await db.get_user_name(telegram_id)
    # количество параметров
    num_params = len(labels)
    # Делим окружность графика на одинаковые части
    # и сохраняем углы для каждой оси
    angles = [n / float(num_params) * 2 * np.pi for n in range(num_params)]
    angles += angles[:1]

    values += values[:1]

    plt.style.use('cyberpunk')
    # создаем полярный график
    fig, ax = plt.subplots(figsize=(16, 13), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=1, marker='o', color='orange')
    ax.fill(angles, values, alpha=0.25)


    perfect_values = [100, 100, 100, 100, 100, 100]
    perfect_values += perfect_values[:1]
    ax.plot(angles, perfect_values, linewidth=1)
    ax.fill(angles, perfect_values, alpha=0.1)

    # оси начинаются с 12 часов
    ax.set_rlabel_position(180 / num_params)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_rlabel_position(0)
    ax.grid(linewidth=5)

    # делаем, так чтобы надписи не "залезали" на график
    for label, angle in zip(ax.get_xticklabels(), angles):
      if angle in (0, np.pi):
        label.set_horizontalalignment('center')
      elif 0 < angle < np.pi:
        label.set_horizontalalignment('left')
      else:
        label.set_horizontalalignment('right')

    plt.xticks(angles[:-1], labels, size=29)

    plt.yticks(
        ticks=list(range(0, 116, 20)),
        labels=list(range(0, 116, 20)),
        size=18)

    ax.set_ylim(0, 115)
    # идеальные значения для атлета
    # ax.plot(angles, perfect_values, color='yellow', linewidth=0.75)
    # ax.fill(angles, perfect_values, color='yellow', alpha=0.25)
    ax.plot(angles, values, color='orange', linewidth=1)
    ax.fill(angles, values, color='orange', alpha=0.25)
    ax.set_title(
        f'{user_info[0]} {user_info[1]}\n Уровень: {user_info[2]}',
        y=1.06,
        fontsize=28,
        fontweight='bold'
        )

    mplcyberpunk.add_glow_effects()
    plt.savefig(f'media/{user_info[0]} {user_info[1]}.png')
    plt.close()


async def months_in_project_histogram():
    """
    Creates histogram with time in project for all active users.
    """
    data = await db.get_data_about_time_in_project()
    today = date.today()
    male_months = defaultdict(int)
    female_months = defaultdict(int)

    for row in data:
        start_date = datetime.strptime(row[0], '%Y-%m-%d').date()
        months = ((today.year - start_date.year) * 12
                  + today.month - start_date.month)
        if row[1] == 'Мужской':
            male_months[months] += 1
        elif row[1] == 'Женский':
            female_months[months] += 1
    plt.figure(figsize=(20, 12))

    months = sorted(set(male_months.keys()) | set(female_months.keys()))

    male_values = [male_months.get(month, 0) for month in months]
    female_values = [female_months.get(month, 0) for month in months]

    plt.bar(months, male_values, label='Парни')
    plt.bar(months, female_values,  bottom=male_values, label='Девушки')

    plt.legend()
    plt.xlabel('Продолжительность тренировок, в месяцах')
    plt.ylabel('Кол-во атлетов')
    plt.title('Гистограмма длительности тренировок в "Прогрессе"')

    # Check if months is not empty
    if months:
        # Set x-axis ticks and grid
        plt.xticks(range(min(months), max(months) + 1, 3))
        plt.grid(axis='both', linestyle='-', which='both', linewidth=3)

        # Set y-axis ticks and grid
        plt.yticks(range(max(max(male_values), max(female_values)) + 1))
    plt.savefig(f'media/time_in_project_hist.png')
    plt.close()


def get_users_ages_and_mean_ages(data: list) -> [int, list]:
    """
    Takes lists of birthdate of users and create a list of ages and mean age
    of users from data.
    """
    users_age = []
    today = date.today()
    for birthdate in data:
        if birthdate[0]:
            age = int(
                (today.year - datetime.strptime(birthdate[0],
                                                '%Y-%m-%d').date().year)
            )
            users_age.append(age)
        else:
            pass
    logging.info(f'List of ages {users_age}')
    logging.info(f'Mean age {np.mean(users_age)}')
    return users_age, np.mean(users_age)


async def ages_of_users_histogram(men_ages: list,
                                  women_ages: list,
                                  men_mean_age: float,
                                  women_mean_age: float):
    """
    Creates 2 histograms for men and users ages.
    """
    men_histogram = defaultdict(int)
    women_histogram = defaultdict(int)
    plt.style.use('cyberpunk')

    # Populate the histograms
    for age in men_ages:
        men_histogram[age] += 1
    for age in women_ages:
        women_histogram[age] += 1

    # Plot the histograms
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    ax1.bar(
        men_histogram.keys(),
        men_histogram.values(),
        align='center',
    )
    ax1.set_xticks(range(min(men_histogram.keys()),
                     max(men_histogram.keys()) + 1, 1))
    ax1.set_yticks(range(min(men_histogram.values()),
                     max(men_histogram.values()) + 1))
    ax1.tick_params(axis='both', labelsize=10, which='both')
    ax1.set_title('Парни', fontsize=16)
    ax1.set_ylabel('Кол-во атлетов', fontsize=14)
    ax1.annotate(f'Cредний возраст: {men_mean_age:.0f} лет', xy=(0.05, 0.9),
                 xycoords='axes fraction', fontsize=12)
    ax1.grid(axis='both', linestyle='-', which='both', linewidth=3)

    ax2.bar(women_histogram.keys(), women_histogram.values(), align='center')
    ax2.set_xticks(range(min(women_histogram.keys()),
                         max(women_histogram.keys()) + 1, 1))
    ax2.set_yticks(range(min(women_histogram.values()),
                         max(women_histogram.values()) + 1))
    ax2.set_title('Девушки', fontsize=16)
    ax2.set_xlabel('Возраст', fontsize=14)
    ax2.set_ylabel('Кол-во атлетов', fontsize=14)
    ax2.grid(axis='both', linestyle='-', which='both', linewidth=3)
    ax2.annotate(f'Cредний возраст: {women_mean_age:.0f} лет', xy=(0.05, 0.9),
                 xycoords='axes fraction', fontsize=12)
    ax2.tick_params(axis='both', labelsize=10, which='both')


    plt.tight_layout()
    plt.savefig(f'media/users_ages.png')
    plt.close()


async def user_weekly_dynamic_graph(telegram_id: int):
    """
    Creates a weekly dynamic graph for user by it's.
    """
    data = await db.get_weekly_dynamic_for_user(telegram_id=telegram_id)

    weeks = [row[0] for row in data]
    results = [row[2] for row in data]
    scaling = [row[3] for row in data]
    fatigue = [row[4] for row in data]

    start_date = datetime(2024, 4, 1)
    dates = [start_date + timedelta(days=7 * (week - 1)) for week in weeks]
    plt.style.use('cyberpunk')

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(dates, results, label='Доволен результатами', marker='o')
    ax.plot(dates, scaling, label='Масштабирование заданий', marker='o')
    ax.plot(dates, fatigue, label='Утомление, мышечная боль', marker='o')

    ax.legend(loc='upper left', fontsize=14)

    # Setting axis intervals and scaling
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,
                                                     interval=4))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%W'))
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.tick_params(axis='both', labelsize=12, which='both')
    ax.set_ylim(0.5, 5.5)
    plt.setp(ax.get_xticklabels(which='both'), rotation=45, ha='right')

    # Set labels and title
    ax.set_xlabel('Дата, номер недели', fontsize=14)
    ax.set_title('Твоя еженедельная динамика состояния', fontsize=14)

    # Adjust spacing between subplots
    plt.tight_layout()
    plt.grid(axis='both', linestyle='-', which='both', linewidth=3)

    # Display the plot
    mplcyberpunk.add_glow_effects(ax)
    plt.savefig(f'media/{telegram_id}_weekly.png')
    plt.close()


async def levels_weekly_dynamic_graph():
    """
    Draws a plot with 3 graphs for 3 different coefficeints for weekly dynamic.
    """
    lvl_one_data = await db.get_weekly_dynamic_for_level(level='Первый')
    lvl_two_data = await db.get_weekly_dynamic_for_level(level='Второй')
    lvl_minkaifa_data = await db.get_weekly_dynamic_for_level(level='Минкайфа')

    weeks_1 = [row[0] for row in lvl_one_data]
    weeks_2 = [row[0] for row in lvl_two_data]
    weeks_mkf = [row[0] for row in lvl_minkaifa_data]
    start_date = datetime(2024, 4, 1)

    dates_1 = [
        start_date + timedelta(days=7 * (week - 1)) for week in weeks_1]
    dates_2 = [
        start_date + timedelta(days=7 * (week - 1)) for week in weeks_2]
    dates_mkf = [
        start_date + timedelta(days=7 * (week - 1)) for week in weeks_mkf]

    lvl_one_results = [row[2] for row in lvl_one_data]
    lvl_one_scaling = [row[3] for row in lvl_one_data]
    lvl_one_fatigue = [row[4] for row in lvl_one_data]

    lvl_two_results = [row[2] for row in lvl_two_data]
    lvl_two_scaling = [row[3] for row in lvl_two_data]
    lvl_two_fatigue = [row[4] for row in lvl_two_data]

    lvl_minkaifa_results = [row[2] for row in lvl_minkaifa_data]
    lvl_minkaifa_scaling = [row[3] for row in lvl_minkaifa_data]
    lvl_minkaifa_fatigue = [row[4] for row in lvl_minkaifa_data]

    plt.style.use('cyberpunk')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 9))

    # results graph for all 3 levels
    ax1.plot(dates_1, lvl_one_results, label='Первый', marker='o')
    ax1.plot(dates_2, lvl_two_results, label='Второй', marker='o')
    ax1.plot(dates_mkf, lvl_minkaifa_results, label='Минкайфа', marker='o')
    ax1.legend(fontsize=14, loc='upper right')

    # Setting axis intervals and scaling
    ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,
                                                     interval=4))
    ax1.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax1.xaxis.set_minor_formatter(mdates.DateFormatter('%W'))
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax1.tick_params(axis='both', labelsize=12, which='both')
    ax1.set_ylim(0.5, 5.5)
    plt.setp(ax1.get_xticklabels(which='both'), rotation=45, ha='right')

    # Set labels and title
    ax1.set_title('Удовлетворение результатами тренировок', fontsize=14)

    # scaling graph for all 3 levels
    ax2.plot(dates_1, lvl_one_scaling, label='Первый', marker='o')
    ax2.plot(dates_2, lvl_two_scaling, label='Второй', marker='o')
    ax2.plot(dates_mkf, lvl_minkaifa_scaling, label='Минкайфа', marker='o')

    # Setting axis intervals and scaling
    ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,
                                                     interval=4))
    ax2.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax2.xaxis.set_minor_formatter(mdates.DateFormatter('%W'))
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax2.tick_params(axis='both', labelsize=12, which='both')
    ax2.set_ylim(0.5, 4.5)
    plt.setp(ax2.get_xticklabels(which='both'), rotation=45, ha='right')

    # Set labels and title
    ax2.set_title('Масштабирование тренировок', fontsize=14)

    # scaling graph for all 3 levels
    ax3.plot(dates_1, lvl_one_fatigue, label='Первый', marker='o')
    ax3.plot(dates_2, lvl_two_fatigue, label='Второй', marker='o')
    ax3.plot(dates_mkf, lvl_minkaifa_fatigue, label='Минкайфа', marker='o')

    # Setting axis intervals and scaling
    ax3.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO,
                                                      interval=4))
    ax3.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax3.xaxis.set_minor_formatter(mdates.DateFormatter('%W'))
    ax3.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax3.tick_params(axis='both', labelsize=12, which='both')
    ax3.set_ylim(0.5, 5.5)

    ax1.grid(axis='both', linestyle='-', which='both', linewidth=3)
    ax2.grid(axis='both', linestyle='-', which='both', linewidth=3)
    ax3.grid(axis='both', linestyle='-', which='both', linewidth=3)

    plt.setp(ax3.get_xticklabels(which='both'), rotation=45, ha='right')

    # Set labels and title
    ax3.set_title('Утомление, мышечная боль', fontsize=14)
    ax3.set_xlabel('Дата, номер недели', fontsize=14)

    # Adjust spacing between subplots

    # Display the plot
    mplcyberpunk.add_glow_effects(ax1)
    mplcyberpunk.add_glow_effects(ax2)
    mplcyberpunk.add_glow_effects(ax3)

    plt.tight_layout(pad=0.8, w_pad=1, h_pad=1.0)
    plt.savefig(f'media/levels_weekly.png')
    plt.close()
