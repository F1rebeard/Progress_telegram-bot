from datetime import date, datetime
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
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
    months = range(
        max(max(male_months.values()), max(female_months.values()) + 1)
    )

    months = sorted(set(male_months.keys()) | set(female_months.keys()))

    male_values = [male_months.get(month, 0) for month in months]
    female_values = [female_months.get(month, 0) for month in months]

    plt.bar(months, male_values, color='b', alpha=0.5, label='Парни')
    plt.bar(months, female_values, color='r', alpha=0.5, bottom=male_values,
            label='Девушки')

    plt.legend()
    plt.xlabel('Продолжительность тренировок, в месяцах')
    plt.ylabel('Кол-во атлетов')
    plt.title('Гистограмма длительности тренировок в "Прогрессе"')

    # Set x-axis ticks and grid
    plt.xticks(range(min(months), max(months) + 1))
    plt.grid(axis='x', linestyle='--')

    # Set y-axis ticks and grid
    plt.yticks(range(max(max(male_values), max(female_values)) + 1))
    plt.grid(axis='y', linestyle='--')

    plt.show()
    plt.savefig(f'/media/time_in_project_hist.png')
    plt.close()


def get_men_and_women_ages_and_mean_ages(data: list)

# for birthdate in data:
#     if birthdate[0]:
#         age = int(
#             (today.year - datetime.strptime(birthdate[0],
#                                             '%Y-%m-%d').date().year)
#         )
#         men_age.append(age)
#     else:
#         pass
# logging.info(f'Mean age {np.mean(men_age)}')
# return men_age, np.mean(men_age)
