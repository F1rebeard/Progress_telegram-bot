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
    plt.savefig(f'media/{telegram_id}.png')
    plt.close()



