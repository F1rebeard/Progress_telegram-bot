import os

from dotenv import load_dotenv

load_dotenv()

admin_list = os.getenv("ADMIN_IDS")
ADMIN_IDS = list(map(int, admin_list.split(', ')))

#exercies urls
RELIZ_URL = 'https://youtube.com/playlist?list=PLz5r9FgBibzZhDp-CT3pBsI5_Lnm9HhL0&si=3rz4K6UzVV24_Y7D'
ACTIVATION_URL = 'https://youtube.com/playlist?list=PLz5r9FgBibzYa0S2kqNvOC1hN8pqWj5qT&si=_LP-g2AwNRKmZF6e'
PREACTIVATION_URL = 'https://youtube.com/playlist?list=PLz5r9FgBibzaHjlgqTM_fb8PaDJ727xgO&si=hTEc5JeoX0QYByQD'
UPPER_ACTIVATION_URL = 'https://youtu.be/MoMScRBVhns?si=in9J3plVCS2Fxtsh'
LOWER_ACTIVATION_URL = 'https://youtu.be/mb2HI-1yaa4?si=sOq8UdXxodz7uR_a'
PLZ_ACTIVATION_URL = 'https://youtu.be/kDy3muAqfo8?si=gGk9mHNxlRCi_Ycf'
LAY_DOWN_BREATH_URL = 'https://youtu.be/wh2wvSFVxzU?si=NyWD-8CfJgHb_53k'
LAY_DOWN_CORE = 'https://youtu.be/N2xrj1wd8vk?si=MryEAYIou14Miez2'
LATS_ACTIVATION_URL = 'https://youtu.be/wH729BqNUsM?si=4SbSq7i6zMZ3sqec'
GPSH_PULL_URL = 'https://youtu.be/Mpr-j2WN9lU?si=uyKo9i95lH24Lxty'
FOOT_ACTIVATION_URL = 'https://youtu.be/mb2HI-1yaa4?list=PLz5r9FgBibzYa0S2kqNvOC1hN8pqWj5qT&t=292'

# warm up protocols
WARM_UP_PROTOCOL_1: str = f'<b>Длительная аэробная работа,' \
      f' техническая работа на гребном</b>\n\n' \
      '🔶 Активация мышц кора через дыхание: ' \
      f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
      f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>,'\
      ' промять ребра (3-5 мин) \n\n' \
      '🔶 Лёгкая аэробная работа на нужном снаряде' \
      ' (3-6 мин)\n\n' \
      f'🔶 <b>Интервалы</b> в режиме работа:отдых 1:1, работать на мощности' \
      ' ступени отказа или ИВН 5-6 (3-5 мин) \n\n' \
      f'🔶 <b>Опция:</b> суставная разминка,' \
      f' <a href="{RELIZ_URL}">релиз</a>' \
      ' уставших/забитых мышц: по необходимости (5 мин)'

WARM_UP_PROTOCOL_2: str = f'<b>Аэробная интервальная</b>\n' \
      'Интервальная работа высокой интенсивности\n' \
      'Отличия от равномерной и низкоинтенсивной:' \
      ' на разминке надо подышать и позакисать.' \
      ' Продуваем сопло!\n\n' \
      '🔶 Активация мышц кора через дыхание: ' \
      f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
      f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>,'\
      ' промять ребра (3-5 мин) \n\n' \
      '🔶 Лёгкая аэробная работа на нужном снаряде' \
      ' (3-5 мин)\n\n' \
      f'🔶 <b>Интервалы</b> в режиме работа:отдых 1:1, работать на мощности' \
      ' ступени отказа\n\n' \
      '🔶 Ускорения 20-30 секунд на 120-130% ' \
      'от предполагаемой скорости/мощности ИВН 6-7,' \
      ' пульс 75-85% максимума (3-5 мин)\n\n' \
      f'🔶 <b>Опция:</b> суставная разминка,' \
      f' <a href="{RELIZ_URL}">релиз</a>' \
      ' уставших/забитых мышц: по необходимости (5 мин)'

WARM_UP_PROTOCOL_3: str = f'<b>Силовая для ПЛ: тяги, приседания, жимы</b>\n\n' \
     f'🔶 Суставная разминка для основных суставов:' \
     f' плеч, локтей, запястий, таза, коленей, голеней,' \
     f' активные вращательные и амплитудно-маховые' \
     f' движения (3-5 мин)\n\n' \
     '🔶 Активация мышц кора через дыхание: ' \
     f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
     f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>,'\
     ' промять ребра (3-5 мин) \n\n' \
     f'🔶 Если есть боль или дискомфорт: выполнить релиз мышц,' \
     f' которые будут работать' \
     f' (см. видео с <a href="{RELIZ_URL}">релизом</a> и '\
     f' активацию<a href="{UPPER_ACTIVATION_URL}">верха</a> и'\
     f' <a href="{LOWER_ACTIVATION_URL}">низа</a>) '\
     f'(5-6 мин)\n\n'\
     '🔶 Динамичная круговая разминка (ДКР) на нужные мышцы' \
     ' с рабочим снарядом (гриф, гантели):' \
     ' приседания, жимы, наклоны (3-5 кругов по 10-15 пвт)\n\n'\
     '🔶 Подготовка к целевому упражнению: старт с грифа,' \
     ' добавлять вес до рабочего, шаг произвольный\n\n' \
     f'⚠ <b>Важно</b>: в ПЛ-упражнениях после 70%' \
     f' от максимального веса на разминке можно делать' \
     f' 50-60% повторений\n\n' \
     'Пример: присед 80% (100 кг) 3 по 8, начиная с веса 70 кг'\
     ' (70%) делаем 3-4 разминочных повтора, а не по 8\n\n'\
     'Исключение: низкоповторная работа (2-5 повторений)\n\n' \
     f'🔶 <b>Опция:</b> гиперэкстензии, разгибания голени или'\
     ' локтевых суставов'

WARM_UP_PROTOCOL_4: str = f'<b>Силовая для ТА</b>\n'\
       f'Отличия от ПЛ: надо готовить плечи'\
       ' для амплитудной работы\n\n'\
       '🔶 Суставная разминка для основных суставов: плеч,'\
       ' локтей, запястий, таза, коленей, голеней,' \
       ' активные вращательные и амплитудно-маховые' \
       ' движения (3-5 мин)\n\n'\
       '🔶 Активация мышц кора через дыхание: ' \
       f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
       f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>,'\
       ' промять ребра (3-5 мин) \n\n' \
       '🔶 Если есть боль или' \
       ' дискомфорт: релиз мышц, которые будут работать' \
       f' (см. видео с <a href="{RELIZ_URL}">релизом</a> и'\
       f' активацию <a href="{UPPER_ACTIVATION_URL}">верха</a> и'\
       f' <a href="{LOWER_ACTIVATION_URL}">низа</a>)'\
       f' (5-6 мин)\n\n'\
       '🔶 Включение мышц ПЛЗ: нижней трапы, зубчатой,'\
       ' мышц манжеты '\
       f'(см. <a href="{PLZ_ACTIVATION_URL}">видео</a>'\
       f' «Активация плеча и лопатки») (2-3 подхода на'\
       ' мышцу, 4-6 минут)\n\n' \
       '🔶 Динамичная круговая разминка (ДКР) на '\
       'нужные мышцы с рабочим снарядом (гриф, гантели):'\
       ' приседания, жимы, наклоны (3-5 кругов' \
       ' по 10-15 пвт)\n\n' \
       '🔶 Подводящие упражнения: толчковые и рывковые '\
       'тяги с пола и с виса, жимы из-за головы, в '\
       'круговом формате, вес ок. 25-40% рабочего, легкое'\
       ' утомление (3-4 подхода, 3-5 минут)\n\n'\
       '🔶 Подготовка к целевому упражнению, старт с '\
       'грифа, добавлять вес до рабочего, шаг произвольный\n\n'\
       f'🔶 <b>Опция:</b> гиперэкстензии, разгибания '\
       'голени или локтевых суставов (3 подхода, 3-5 мин)'\

WARM_UP_PROTOCOL_5: str = f'<b>Гимнастика</b>\n\n'\
       f'🔶 Суставная разминка для основных суставов:'\
       f' плеч, локтей, запястий, таза, активные'\
       f' вращательные и амплитудно-маховые движения'\
       f' (3-5 мин)\n\n'\
       '🔶 Активация мышц кора через дыхание: ' \
       f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
       f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>,'\
       ' промять ребра (3-5 мин) \n\n' \
       '🔶 Если есть боль или' \
       ' дискомфорт: релиз мышц, которые будут работать' \
       f' (см. видео с <a href="{RELIZ_URL}">релизом</a> и '\
       f'<a href="{UPPER_ACTIVATION_URL}">активацию верха</a>)\n\n'\
       f'🔶 Включение мышц ПЛЗ: нижней трапы, зубчатой, мышц'\
       f' манжеты (см. <a href="{PLZ_ACTIVATION_URL}">видео</a>'\
       f' «Активация плеча и лопатки»)\n (2-3 подхода на'\
       ' мышцу, 4-6 минут)\n\n' \
       'В приоритете полноамплитудная работа с резиной, легкими '\
       'гантелями.\n При работе с перекладиной: '\
       f'<a href="{LATS_ACTIVATION_URL}">активация широчи</a>, '\
       f'<a href="{GPSH_PULL_URL}">тяга на ГПШ</a>\n\n' \
       f'🔶 Динамичная круговая разминка (ДКР) на'\
       'мышцы кора и плечевого: отжимания от пола и на брусьях'\
       'сит-апы, маховые движения на кольцах и перекладине '\
       '(3-5 кругов до локального утомления, 3-4 мин)\n\n'\
       '🔶 Основное упражнение: отработать в низкоповторном'\
       ' режиме (по необходимости)\n\n'\
       '⚠ <b>Важно:</b> при многоповторной гликолитической'\
       ' гимнастике мышцы на разминке нужно прогреть и'\
       f' "запампить", это значительно <b>снизит риск</b>'\
       'травмы и поможет выложиться на 100%'

WARM_UP_PROTOCOL_6: str = f'<b>Метконы</b>\n'\
    'Основа разминки - интервальная аэробика,'\
    ' дополнительно подключаем разминку для силовых/гимнастических упражнений,'\
    ' которые будут в комплексе\n\nЧем интенсивнее комплекс - тем больше'\
    ' внимания разминке, особенно прогревочным интервалам\n\n'\
    '🔶 Активация мышц кора через дыхание: ' \
    f'<a href="{LAY_DOWN_BREATH_URL}">подышать лёжа</a>'\
    f' вместе с <a href="{LAY_DOWN_CORE}">изо на пресс</a>, '\
    'промять ребра (3-5 мин) \n\n' \
    '🔶 Легкая аэробная работа на байке или гребле (4-5 минут)\n\n' \
    '🔶 Интервалы на байке или гребле работа:отдых 1:1 или 1:2 (4-5 мин)\n\n'\
    f'🔶 <b>Если нужно</b> включение мышц стопы и латеральной линии (см.'\
    f'<a href="{FOOT_ACTIVATION_URL}">видео</a>) (2-3 подхода, 3-5 мин)\n\n'\
    f'🔶 <b>Если нужно</b> включение мышц ПЛЗ: нижней трапы, зубчатой, мышц'\
    f' манжеты плеча (см. <a href="{PLZ_ACTIVATION_URL}">видео</a>)\n'\
    f'В приоритете полноамплитудная работа с резиной, легкими гантелями\n'\
    f'При работе с перекладиной:'\
    f' <a href="{LATS_ACTIVATION_URL}">активация широчи</a>, '\
    f'<a href="{GPSH_PULL_URL}">тяга на ГПШ</a> (2-3 подхода, 3-5 мин)\n\n' \
    f'🔶 Динамичная круговая разминка (ДКР): легкие упражнения со снарядами'\
    f' и весом тела, задействовать мышцы, которые понадобятся в комплексе\n'\
    '(3-5 кругов, до 5-6 минут, между кругами можно делать паузы отдыха\n\n'\
    f'🔶 Прогревочные интервалы: после общей разминки и разогрева выполнить' \
    f' рабочие упражнения с акцентом на высокий (рабочий) темп и быстрые ' \
    'переходы (3-6 интервалов, не дольше 10-15 минут с учетом пауз отдыха между)'

PROGRESS_LEVELS = {
    'Первый': '1',
    'Второй': '2',
    'Минкайфа': '4',
    'Соревнования': '3',
}

WEEKDAYS = {
    1: 'пнд',
    2: 'втр',
    3: 'срд',
    4: 'чтв',
    5: 'птн',
    6: 'сбт',
    7: 'вск'
}

RUS_MONTHS = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}
#Предактивации
PREACTIVATIONS_BTNS = (
    ('Диафрагма', 'https://youtu.be/wh2wvSFVxzU?si=rG3GfCYG_bvKPV1n'),
    ('Диафрагма со жгутом', 'https://youtu.be/rqFQdf9vX_g?si=vlYk56X_ehaCVgC7'),
    ('Косые. Планка', 'https://youtu.be/_i3lfmlGDlA?si=jaZZf6ySawbKyvDq'),
    ('Косые. Ротация', 'https://youtu.be/5O1t212VH40?si=Us8OECGlH5Y1An8s'),
    ('Малая круглая', 'https://youtu.be/SiJMSTiRYJM?si=TfENxOT0msNJC_SL'),
    ('Надостная', 'https://youtu.be/dAMIHf9bWeI?si=JgqYfWgnJTWOb1im'),
    ('Нижняя трапеция', 'https://youtu.be/wYWbjFrw48Q?si=_xGpPQJvV5i1qEIl'),
    ('Подошвенный сгибатель пальцев', 'https://youtu.be/p2s5xAJ5qwM?si=zjfyAzGsYnV45k15'),
    ('Подлопаточная', 'https://youtu.be/lfpsuVD38hk?si=8buYVORoLtJeAUeT'),
    ('Подостная', 'https://youtu.be/FFbsW1gkcTo?si=HWjJv220hyTa_JEU'),
    ('Пресс, верхняя изоляция', 'https://youtu.be/N2xrj1wd8vk?si=v36YlGT8pQfbNX0N'),
    ('Пресс, нижняя изоляция', 'https://youtu.be/vnb2YG69zAQ?si=nLGgECu4Z0FpfN5e'),
    ('Ромбовидные', 'https://youtu.be/2W5frVqrjqs?si=ypha5K1GJkrqCnuf'),
    ('Средняя ягодичная', 'https://youtu.be/aK1qvID61Nc?si=BtNKeLgNOo9kuU0c'),
    ('Cтопа и ягодичная', 'https://youtu.be/LQiW1s8Ug8c?si=VtbU8k902Iad87_j')
)

#Активации
ACTIVATIONS_BTNS = (
    ('Включение верха', 'https://youtu.be/MoMScRBVhns?si=_zUbLhIu27YEbrwb'),
    ('Включение низа', 'https://youtu.be/mb2HI-1yaa4?si=8dTZUrIeFzKs7z6f'),
    ('Активация перед беговой тренировкой', 'https://www.youtube.com/watch?v=QOYiWQS5VGs'),
    ('Активация широчайшей для подтягиваний', 'https://www.youtube.com/watch?v=wH729BqNUsM'),
    ('Активация ПЛЗ', 'https://www.youtube.com/watch?v=kDy3muAqfo8'),
)

#Релиз
RELEASES_BTNS = [
    ('Большая грудная', 'https://www.youtube.com/watch?v=Fxv2DQTtveQ'),
    ('Голень спереди', 'https://www.youtube.com/watch?v=On8rsKNByHs'),
    ('Грудной отдел позвоночника', 'https://www.youtube.com/watch?v=FMFmiViRTYA'),
    ('Дельтовидные', 'https://www.youtube.com/watch?v=2KlGPKsYcBc'),
    ('Задняя поверхность бедра', 'https://www.youtube.com/watch?v=6mMO3oxxsuU'),
    ('Икроножная и камбаловидная', 'https://www.youtube.com/watch?v=MvttpzUUGQY'),
    ('Квадрицепс', 'https://www.youtube.com/watch?v=Kip_0YzsTmc'),
    ('Квадратная мышца поясницы', 'https://www.youtube.com/watch?v=g5u-S3qznmE'),
    ('Кисть Тенара', 'https://www.youtube.com/watch?v=4NlR1VPlIcA'),
    ('Клювовидно-плечевая', 'https://www.youtube.com/watch?v=1mVwu_pwp_0'),
    ('Малая грудная', 'https://www.youtube.com/watch?v=eWNAbr-7KRk'),
    ('Передняя зубчатая', 'https://www.youtube.com/watch?v=ZvTQWibijTY'),
    ('Подключичная', 'https://www.youtube.com/watch?v=zWpJfqc1moM'),
    ('Приводящие', 'https://www.youtube.com/watch?v=9TEqWmdtPbk'),
    ('Стопы', 'https://www.youtube.com/watch?v=oY9uuhCIY8E'),
    ('Трапеция', 'https://www.youtube.com/watch?v=uXbG4gHXKdc'),
    ('Трицепс', 'https://www.youtube.com/watch?v=yTj9VxYYb60'),
    ('Ягодичные', 'https://www.youtube.com/watch?v=cgRaQp8iljQ')
]

#Техника упражнений
EXERCISES_BTNS = [
    ('Безопасный подъем по канату', 'https://www.youtube.com/watch?v=I2GRhHq4PK8'),
    ('ГБ, подъем на длинную головку бицепса', 'https://www.youtube.com/watch?v=X7IrkhUiAbU'),
    ('Квадратная тяга', 'https://youtu.be/mCOs4yQaDP4?si=qOOptRqWZofF1CYp'),
    ('Кикбоксер, ножницы и уголок на перекладине', 'https://www.youtube.com/watch?v=Qf-h9rhNl-w'),
    ('Отжимания на кольцах из нижней точки', 'https://www.youtube.com/watch?v=UXyWhD61488'),
    ('Пегборд (вис, подтягивания без/c ногами)', 'https://www.youtube.com/watch?v=2yVs4a1SEDk'),
    ('Перехваты на канате с ногами в "замке"', 'https://www.youtube.com/watch?v=lHv36lcKCGg'),
    ('Перехваты на перекладине в висе', 'https://www.youtube.com/watch?v=0NZrX0uS_fw'),
    ('Подтягивание на перекладине из положения активации широчайшей', 'https://www.youtube.com/watch?v=B9NUUHH6gUw'),
    ('Подтягивания ног в кольцах', 'https://www.youtube.com/watch?v=fEs2ioTMH4k'),
    ('Подтягивания на канате с ногами на коробе', 'https://www.youtube.com/watch?v=YtjQLn-Mk70'),
    ('Румынская тяга', 'https://www.youtube.com/watch?v=jRME_wLRl1A'),
    ('Рывок с разных висов в стойку', 'https://www.youtube.com/watch?v=BMhw-FjgwlQ'),
    ('Рывковый уход и рывковый швунг в сед, оверхед', 'https://www.youtube.com/watch?v=sloRSj3IKKY'),
    ('Рывковые тяги (низкая, высокая, китайская)', 'https://www.youtube.com/watch?v=_LRNCUYoRoE'),
    ('Cамолёт', 'https://www.youtube.com/watch?v=B0FHT_Jo0xY'),
    ('Cамолёт в динамике', 'https://www.youtube.com/watch?v=3R8czW28eko'),
    ('Съем и удержание штанги', 'https://www.youtube.com/watch?v=S9bXLb6Kv1I'),
    ('Т-подъемы на среднюю дельту', 'https://www.youtube.com/watch?v=Wb9DU2KGDEo'),
    ('Тяга ГПШ', 'https://www.youtube.com/watch?v=Mpr-j2WN9lU'),
    ('Унилатеральные упражнения с гирей и штангой', 'https://www.youtube.com/watch?v=N7WgYNS4mZw'),
    ('УЯМ, ягодичный марш', 'https://www.youtube.com/watch?v=NjH4Jew78Ok'),
]

#Растяжки
STRETCHING_BTNS = [
    ('Бицепс', 'https://www.youtube.com/watch?v=SGRetti5O5g'),
    ('Большая грудная', 'https://www.youtube.com/watch?v=TpGlvEJECcQ'),
    ('Большая круглая', 'https://www.youtube.com/watch?v=kEIjKuYN1w4'),
    ('Верхняя трапеция', 'https://www.youtube.com/watch?v=c3MXh83HHoA'),
    ('Задняя поверхность бедра', 'https://www.youtube.com/watch?v=f0A4001gCs4'),
    ('Икроножная и камбаловидная', 'https://www.youtube.com/watch?v=p6gxb8-riME'),
    ('Квадрицепс', 'https://www.youtube.com/watch?v=jaS8OCz5Oic'),
    ('Кисть', 'https://www.youtube.com/watch?v=w-gpmWvQVlg'),
    ('Косые', 'https://www.youtube.com/watch?v=A-vqkBkqtzg'),
    ('Лестничные', 'https://www.youtube.com/watch?v=F2feYnI1ka4'),
    ('Малая грудная', 'https://www.youtube.com/watch?v=lw84Acix-uc'),
    ('Передняя дельта', 'https://www.youtube.com/watch?v=eYpdGhShjI4'),
    ('Приводящая', 'https://www.youtube.com/watch?v=VEawOkYa-sU'),
    ('Средняя и задняя дельты', 'https://www.youtube.com/watch?v=5i0VhEKXna4'),
    ('Трицепс', 'https://www.youtube.com/watch?v=fFkQ5ci_rEw'),
    ('Широчайшая', 'https://www.youtube.com/watch?v=meMlHhzazN0'),
    ('Ягодичная', 'https://www.youtube.com/watch?v=jSWwU1PYW7A'),
]

ABBREVIATIONS_DATA = {
    "Анб":
        ("аналогично тач, не разбивать движения от начала до конца", "unbroken"),
    "ГПШ":
        ("Тяга на горизонтальные волокна широчайшей", "gpsh"),
    "ДГБ":
        ("подьъемы на длинную головку бицепса", "dgb"),
    "ДКР":
        ("динамическая круговая разминка", "dkr"),
    "НКП":
        ("подъемы ног к перекладине", "nkp"),
    "ОДВ":
        ("отдых до восстановления, подразумевает время отдыха, достаточное для"
         " выполнения всех рабочих подходов с одинаковой интенсивностью,"
         " психологической стоимостью и за одинаковое время. Рекомендуемый "
         "отдых для силовых упражнений на верх тела составляет 3-5 минут, на"
         " низ 4-6 минут. Рекомендуемый отдых при технической отработке "
         "состалвяет 1 - 1.5 - 2 минуты. Если не прописан иной вариант в"
         " самом задании.", "odv"),
    "ОП":
        ("окислительный потенциал, специфичный уровень силовой выносливости,"
         " определяемый в тесте повторений 70-80% от 1ПМ.", "op"),
    "ПВЗ":
        ("количество повторений в запасе до \"отказа\" в подходе", "pvz"),
    "Подъемы":
        ("подъемы на грудь, взятия на грудь, взятия", "lifts"),
    "Тач":
        ("выполнения упражнения до конца от первого до последнего подхода,"
         " не выпуская снаряд, без сбросов", "touch"),
    "УЯМ":
        ("унилатеральый ягодичный мостик, ягодичный мост на одну ногу", "uyam"),
    "Холлоу":
        ("выполнять упражнение удерживая закрытое положение спины за счет"
         " напряжения мышц кора и ягодиц", "hollow"),
    "ЦДП": ("целевой диапазон повторений", "cdp")
}


