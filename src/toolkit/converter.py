from toolkit import errors

# таблица перевода в базовую ед измерения для длин
LENGTH_TO_METERS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1,
    "km": 1000
}

# таблица перевода в базовую ед измерения для масс
MASS_TO_GRAMS = {
    "g": 1,
    "kg": 1000
}

# функции перевода друг в друга для температур
C_TO_K = lambda c: c + 273.15
K_TO_C = lambda k: k - 273.15
C_TO_F = lambda c: c * 9 / 5 + 32
F_TO_C = lambda f: (f - 32) * 5 / 9
F_TO_K = lambda f: C_TO_K(F_TO_C(f))
K_TO_F = lambda k: C_TO_F(K_TO_C(k))

# таблица перевода в базовую ед измерения (K) для температур
TO_KELVIN = {
    "c": C_TO_K,
    "f": F_TO_K,
    "k": lambda k: k
}

# и из нее
FROM_KELVIN = {
    "c": K_TO_C,
    "f": K_TO_F,
    "k": lambda k: k
}

# для определения группы исходя из единицы измерения
UNIT_TO_GROUP = {}
for unit in LENGTH_TO_METERS:
    UNIT_TO_GROUP[unit] = "length"

for unit in MASS_TO_GRAMS:
    UNIT_TO_GROUP[unit] = "mass"

for unit in FROM_KELVIN:
    UNIT_TO_GROUP[unit] = "temperature"

def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Переводит из одной единицы измерения в другую
    :param value: Исходное числовое значение (int)
    :param from_unit: Исходная ед. измерения (str)
    :param to_unit: Искомая ед. измерения (str)
    :return: Возвращает переведенное в искомую ед. измерения число (float)
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    # проверки на существование ед. измерений
    if from_unit not in UNIT_TO_GROUP:
        raise errors.UnknownUnitError(f"Ошибка! Неизвестная единица: {from_unit}")

    if to_unit not in UNIT_TO_GROUP:
        raise errors.UnknownUnitError(f"Ошибка! Неизвестная единица: {to_unit}")

    # проверка на разные группы
    if not (UNIT_TO_GROUP[from_unit] == UNIT_TO_GROUP[to_unit]):
        raise errors.IncompatibleUnitsError(f"Ошибка! Несовместимые единицы измерения: {from_unit} и {to_unit}")

    group = UNIT_TO_GROUP[from_unit]

    # непосредственно перевод из одной ед. измерения в другую
    if group == "length":
        value *= LENGTH_TO_METERS[from_unit]
        value /= LENGTH_TO_METERS[to_unit]

    elif group == "mass":
        value *= MASS_TO_GRAMS[from_unit]
        value /= MASS_TO_GRAMS[to_unit]

    else:
        value = TO_KELVIN[from_unit](value)
        if value < 0:
            # ниже 0 К быть не может (это абсолютный ноль)
            raise errors.BelowAbsoluteZeroError("Ошибка! Температура ниже абсолютного нуля")
        value = FROM_KELVIN[to_unit](value)

    # возвращаем результат
    return float(value)