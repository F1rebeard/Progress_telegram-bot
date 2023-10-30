NINETY_PERCENTS: int = 90
TEN_PERCENTS: int = 10
ONE_HUNDRED_PERCENTS: int = 100

# Диапазоны для силовых движений для первого уровня
# 0 - Движение, 1 - min мужской, 2 - max мужской, 3 - min женский, 4 - max минский
DEADLIFT_RANGE = ['Cтановая тяга 1ПМ',
                          120, 230, 60, 115,
                          135, 240, 75, 140]
CLEAN_DEADLIFT_RANGE = ['Тяга в толчковых углах 1ПМ',
                                80, 180, 45, 95,
                                110, 210, 55, 105]
SNATCH_DEADLIFT_RANGE = ['Тяга в рывковых углах 1ПМ',
                                 70, 170, 40, 90,
                                 100, 190, 45, 100]
BACK_SQUAT_RANGE = ['Присед 1ПМ',
                            80, 180, 50, 100,
                            100, 205, 60, 120]
FRONT_SQUAT_RANGE = ['Фронтальный присед 1ПМ',
                             70, 170, 40, 95,
                             85, 190, 55, 105]
OVERHEAD_SQUAT_RANGE = ['Оверхед присед 1ПМ',
                                50, 140, 30, 75,
                                70, 150, 40, 85]
PUSH_PRESS_RANGE = ['Жим стоя 1ПМ',
                            40, 95, 20, 65,
                            55, 105, 30, 70]
BENCH_PRESS_RANGE = ['Жим лежа 1ПМ',
                             60, 130, 30, 75,
                             75, 140, 35, 80]

#Диапазон для взрывеной силы для первого уровня
LENGTH_JUMP = ['Прыжок в длину',
               150, 275, 135, 250,
               170, 290, 160, 270]
SNATCH = ['Рывок с пола в сед',
          50, 100, 30, 65,
          65, 125, 40, 75]
POWER_SNATCH = ['Рывок с пола в стойку',
                40, 95, 25, 60,
                60, 105, 35, 65]
POWER_CLEAN = ['Подъем на грудь с пола в стойку',
               60, 120, 35, 75,
               75, 140, 45, 85]
SPLIT_JERK = ['Толчок в ножницы',
              70, 130, 35, 75,
              90, 160, 45, 90]
CLEAN = ['Подъем на грудь с пола в сед',
         70, 130, 35, 80,
         85, 150, 45, 85]
POWER_JERK = ['Жимовой швунг',
              60, 125, 35, 75,
              75, 135, 40, 75]
THRUSTER = ['Трастер со стоек',
            60, 125, 35, 75,
            80, 140, 40, 85]
CLUSTER = ['Кластер с пола',
           55, 120, 30, 75,
           75, 135, 40, 75]
JERK = ['Толчковый швунг',
        60, 125, 35, 75,
        80, 145, 40, 80]
HANG_POWER_SNATCH = ['Рывок с виса в стойку',
                     50, 100, 30, 60,
                     60, 105, 40, 75]
HANG_SNATCH = ['Рывок с виса в сед',
               50, 100, 30, 60,
               65, 125, 35, 65]

# Силовая выносливость
DEADLIFT_CAPACITY = ['Становая 70% от 1ПМ на кол-во',
                     6, 32, 6, 32,
                     6, 32, 6, 32]
SQUAT_CAPACITY = ['Присед 70% от 1ПМ на кол-во',
                  6, 32, 6, 32,
                  6, 32, 6, 32]
PUSH_PRESS_CAPACITY = ['Жим стоя 70% от 1ПМ на кол-во',
                       4, 20, 4, 20,
                       4, 20, 4, 20]
BENCH_PRESS_CAPACITY = ['Жим лежа 70% от 1ПМ на кол-во',
                        5, 20, 5, 20,
                        5, 20, 5, 20]
PULL_UP_CAPACITY = ['Подтягивания с подвесом на кол-во',
                    4, 20, 2, 16,
                    4, 20, 2, 16]
DEEPS_CAPACITY = ['Отжимания  с подвесом на кол-во',
                  4, 20, 2, 16,
                  4, 20, 2, 16]

# Выносливость, эрги
# Время для дальнейшего преобразования вводить в формате чч:мм:сс
TWO_KM_ROW = ['Гребля 2 км',
              '08:30', '07:00', '10:30', '08:00',
              '7:30', '6:35', '9:00', '7:25']
FIVE_KM_ROW = ['Гребля 5 км',
               '22:30', '18:00', '25:00', '21:30',
               '20:30', '16:30', '22:30', '20:30']
TEN_KM_ROW = ['Гребля 10 км',
              '46:00', '38:00', '50:00', '41:30',
              '42:00', '36:30', '46:00', '40:30']
STEP_ROW = ['Гребля ступенчатый',
            160, 360, 90, 270,
            200, 440, 120, 300]
ROW_MAM = ['Гребля МАМ',
           300, 800, 200, 650,
           450, 1000, 250, 750]
ONE_HOUR_ROW = ['Гребля 1 час',
                12857, 15652, 11612, 14400,
                14400, 16216, 12857, 14754]
TEN_MIN_ROW = ['Гребля 10 минут',
               120, 200, 80, 150,
               150, 250, 100, 175]
BIKE_STEP = ['Байк ступенчатый',
             160, 440, 90, 330,
             120, 200, 80, 160]
BIKE_MAM = ['Байк МАМ',
            400, 1400, 250, 1000,
            650, 1999, 350, 1200]
TEN_MIN_BIKE = ['Байк 10 минут',
                100, 180, 60, 140,
                120, 200, 80, 160]
SKI_STEP = ['Лыжи ступенчатый',
            120, 320, 90, 240,
            160, 360, 120, 270]
SKI_MAM = ['Лыжи МАМ',
           300, 750, 150, 500,
           400, 850, 200, 600]
TEN_MIN_SKI = ['Лыжи 10 минут',
               100, 180, 60, 140,
               125, 220, 100, 160]

# Гимнастика
# для движений, где минимальный порог равен одному повторению
# сделать диапазон от 0% до 100% где 0 - 0%
PULL_UP_RM = ['Строгие подтягивания 1ПМ',
              5, 50, 1, 25,
              15, 60, 1, 35]
PULL_UPS = ['Подтягивания за 1 подход',
            5, 30, 1, 25,
            7, 32, 3, 25]
STRICT_HS_PUSH_UPS = ['Строгие отжимания в стойке за 1 подход',
                      3, 30, 1, 15,
                      5, 45, 3, 25]
L_SIT = ['Уголок в упоре на полу',
         5, 45, 5, 45,
         10, 60, 5, 45]
HANG_L_SIT = ['Вис в уголке',
              10, 75, 10, 75,
              20, 90, 20, 90]
HS_WALK = ['Ходьба на руках за 1 проход',
           1, 30, 1, 20,
           10, 45, 5, 30]
MIN_HS_WALK = ['Ходьба на руках за 1 минуту',
               0, 30, 1, 25,
               10, 45, 5, 30]
HANG = ['Вис на перекладине',
        45, 180, 30, 150,
        60, 300, 60, 180]
ROPES = ['Канаты 4.5 метра с ногами за 2 минуты',
         3, 12, 2, 8,
         5, 15, 3, 12]
NINETY_SEC_RING_MUSCLE_UPS = ['Выходы на кольцах за 90 секунд',
                              1, 20, 1, 8,
                              4, 25, 1, 8]
NINETY_SEC_MUSCLE_UPS = ['Выходы на перекладине за 90 секунд',
                         1, 25, 1, 12,
                         6, 30, 1, 12]
RING_DEEP_RM = ['Отжимания на кольцах 1ПМ',
                5, 45, 1, 20,
                10, 60, 1, 20]
DEEP_RM = ['Отжимания на брусьях 1ПМ',
           10, 65, 5, 30,
           15, 75, 5, 30]
HS_PUSH_UPS = ['Отжимания в стойке кипом за 1 подход',
               3, 40, 3, 30,
               10, 50, 5, 35]
TOES_TO_BAR = ['НКП за 1 подход',
               5, 40, 3, 35,
               15, 55, 10, 40]
RING_MUSCLE_UPS = ['Выходы на кольцах за 1 подход',
                   1, 15, 1, 8,
                   3, 22, 3, 12]
MUSCLE_UPS = ['Выходы на перекладине за 1 подход',
              1, 12, 0, 20,
              5, 28, 3, 18]
STRICT_RING_MUSCLE_UPS = ['Строгие выходы на кольцах за 1 подход',
                          1, 8, 1, 5,
                          1, 12, 1, 8]
LEGLESS_ROPES = ['Канаты 4.5 метра без ног за 2 минуты',
                 2, 10, 1, 6,
                 4, 12, 1, 8]

# Metcons
ONE_HUNDRED_AND_FIFTY_BURPEES = ['150 бурпи с прыжком +15 см',
                                 '15:30', '09:00', '16:30', '09:30',
                                 '12:30', '07:30', '14:00', '08:30']
KAREN = ['Карен',
         '12:00', '06:30', '12:00', '06:30',
         '10:00', '04:50', '10:00', '05:30']
MURPH = ['Мерф',
         '01:15:00', '40:00', '01:30:00', '45:00',
         '01:05:00', '32:00', '01:10:00', '38:00' ]
CINDY = ['Синди',
         300, 900, 240, 840,
         450, 1050, 300, 990]
LINDA = ['Линда',
         '35:00', '17:00', '35:00', '17:00',
         '25:00', '15:00', '25:00', '16:30']
OPEN_13_1 = ['Open 13.1',
             120, 240, 120, 240,
             200, 330, 150, 300
             ]
KALSU = ['Калсу',
         '01:30:00', '30:00', '01:30:00', '30:00',
         '60:00', '20:00', '60:00', '25:00']
# поправить оупены
OPEN_19_1 = ['Open 19.1',
             152, 304, 114, 266,
             228, 342, 190, 304]
OPEN_16_5 = ['Open 16.5',
             '18:00', '10:30', '20:00', '11:30',
             '14:00', '09:30', '15:00', '10:30']

TIME_MOVEMENTS = ['Гребля 2 км', 'Гребля 5 км', 'Гребля 10 км',
                  '150 бурпи с прыжком +15 см', 'Карен', 'Мерф', 'Линда',
                  'Калсу', 'Open 16.5']


POWER_RANGES = [
    LENGTH_JUMP,
    SNATCH,
    POWER_SNATCH,
    POWER_CLEAN,
    SPLIT_JERK,
    CLEAN,
    POWER_JERK,
    THRUSTER,
    CLUSTER,
    JERK,
    HANG_POWER_SNATCH,
    HANG_SNATCH
]

# Список из диапазонов для силовых упражнений
STRENGTH_RANGES = [
     DEADLIFT_RANGE,
     CLEAN_DEADLIFT_RANGE,
     SNATCH_DEADLIFT_RANGE,
     BACK_SQUAT_RANGE,
     FRONT_SQUAT_RANGE,
     OVERHEAD_SQUAT_RANGE,
     PUSH_PRESS_RANGE,
     BENCH_PRESS_RANGE,
]

STRENGTH_CAPACITY_RANGES = [
    DEADLIFT_CAPACITY,
    SQUAT_CAPACITY,
    PUSH_PRESS_CAPACITY,
    BENCH_PRESS_CAPACITY,
    PULL_UP_CAPACITY,
    DEEPS_CAPACITY
]

AEROBIC_RANGES = [
    TEN_MIN_SKI,
    TEN_MIN_BIKE,
    TEN_MIN_ROW,
    TWO_KM_ROW,
    FIVE_KM_ROW,
    TEN_KM_ROW,
    ONE_HOUR_ROW,
    STEP_ROW,
    SKI_MAM,
    SKI_STEP,
    ROW_MAM,
    BIKE_MAM,
    BIKE_STEP,
]

GYMNASTIC_RANGES = [
    PULL_UP_RM,
    PULL_UPS,
    STRICT_HS_PUSH_UPS,
    L_SIT,
    HANG_L_SIT,
    HS_WALK,
    MIN_HS_WALK,
    HANG,
    ROPES,
    NINETY_SEC_RING_MUSCLE_UPS,
    NINETY_SEC_MUSCLE_UPS,
    RING_DEEP_RM,
    DEEP_RM,
    HS_PUSH_UPS,
    TOES_TO_BAR,
    RING_MUSCLE_UPS,
    MUSCLE_UPS,
    STRICT_RING_MUSCLE_UPS,
    LEGLESS_ROPES
]

METCON_RANGES = [
    ONE_HUNDRED_AND_FIFTY_BURPEES,
    KAREN,
    MURPH,
    CINDY,
    LINDA,
    OPEN_13_1,
    KALSU,
    OPEN_19_1,
    OPEN_16_5
]

CATEGORIES_VIA_RANGES = {
    "METCON_RANGES": 'Метконы',
    "GYMNASTIC_RANGES": 'Гимнастика',
    "AEROBIC_RANGES": 'Выносливость и эргометры',
    "STRENGTH_CAPACITY_RANGES": 'Силовая выносливость',
    "POWER_RANGES": 'Взрывная сила',
    "STRENGTH_RANGES": 'Сила'
}

# basic exercises and movements
BASE_STRENGTH_RANGES = [
     DEADLIFT_RANGE,
     BACK_SQUAT_RANGE,
     FRONT_SQUAT_RANGE,
     OVERHEAD_SQUAT_RANGE,
     PUSH_PRESS_RANGE,
     BENCH_PRESS_RANGE,
]

BASE_POWER_RANGES = [
    LENGTH_JUMP,
    SNATCH,
    POWER_SNATCH,
    POWER_CLEAN,
    SPLIT_JERK,
    POWER_JERK,
    THRUSTER,
    CLEAN,
]

BASE_STRENGTH_CAPACITY_RANGES = [
    DEADLIFT_CAPACITY,
    SQUAT_CAPACITY,
    PUSH_PRESS_CAPACITY,
    BENCH_PRESS_CAPACITY,
    PULL_UP_CAPACITY,
    DEEPS_CAPACITY
]

BASE_AEROBIC_RANGES = [
    TWO_KM_ROW,
    FIVE_KM_ROW,
    STEP_ROW,
    ROW_MAM,
    BIKE_MAM,
    BIKE_STEP,
]

BASE_GYMNASTIC_RANGES = [
    PULL_UP_RM,
    HS_WALK,
    MIN_HS_WALK,
    HANG,
    ROPES,
    NINETY_SEC_RING_MUSCLE_UPS,
    NINETY_SEC_MUSCLE_UPS,
    DEEP_RM,
    TOES_TO_BAR,
    MUSCLE_UPS,
    LEGLESS_ROPES
]

BASE_METCON_RANGES = [
    ONE_HUNDRED_AND_FIFTY_BURPEES,
    OPEN_13_1,
    OPEN_16_5,
    CINDY,
]

MINKAIF_LVL_ONE_USERS = [
    5687110,
    24545281,
    39216101,
    53446953,
    56995625,
    138354650,
    219813598,
    224060833,
    274928384,
    307592655,
    330067834,
    394551466,
    430885909,
    508664245,
    558389121,
    591169856,
    641891302,
    642067063,
    696524114,
    706074374,
    709002847,
    861856636,
    865009374,
    912227910,
    975526658,
    1442382006
]

MINKAIF_LVL_TWO_USERS = [
    272950301,
    455384939,
    620071602,
    765563507,
    1008095334,
]
