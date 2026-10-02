from dataclasses import dataclass

from toolkit import errors


@dataclass
class Token:
    type: str
    value: object = None

def match_simbol(char: str) -> str:
    """
    Для символов + - * / возвращает соответствующее значение type для токена
    :param char: Входной символ (str)
    :return: Значение type (str) для этого символа
    """

    types = {"+": "PLUS",
             "-": "MINUS",
             "*": "STAR",
             "/": "SLASH"}
    return types[char]

def tokenize(expression: str) -> list[Token]:
    """
    Разделяет входное выражение на токены.

    :param expression: Входное выражение (str)
    :return: Список готовых токенов (list)
    """

    tokens: list[Token] = []
    i = 0
    n = len(expression)
    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1

        elif char.isdigit():
            number = ""
            dot_count = 0
            while char.isdigit() or char == "." and dot_count <= 1:
                number+=char
                i += 1
                if i >= n:
                    break
                char = expression[i]
                if char == ".": dot_count+=1

            new_token = Token(type="NUMBER", value=float(number))
            tokens.append(new_token)

        elif char in "+-*/":
            if len(tokens) == 0:
                if char in "+-":
                    if char == "+":
                        i += 1
                    else:
                        i += 1
                        tokens.append(Token(type="UNARY_MINUS"))
                else:
                    i += 1
                    tokens.append(Token(type=match_simbol(char)))


            elif char in "+-" and tokens[-1].type != "NUMBER":
                if char == "+":
                    i += 1
                else:
                    i+=1
                    tokens.append(Token(type="UNARY_MINUS"))
            else:
                tokens.append(Token(type=match_simbol(char)))
                i += 1

        else:
            raise errors.InvalidCharacterError(f"Ошибка! Недопустимый символ: {char}!")

    return tokens

def validate(tokens: list[Token]) -> None:
    """
    Проверяет список токенов на правильное арифметическое выражение
    :param tokens: Список токенов (list)
    :return: None, т.к. только проверяет и, если что-то не так, выдает ошибку
    """

    if not tokens:
        raise errors.EmptyExpressionError("Ошибка! Пустое выражение")

    state = True

    for token in tokens:
        if state:
            if token.type != "NUMBER" and token.type != "UNARY_MINUS":
                raise errors.MissingOperandError("Ошибка! Пропущенный операнд")
            elif token.type == "NUMBER":
                state = False

        else:
            if token.type != "NUMBER":
                state = True

            else:
                raise errors.MissingOperatorError("Ошибка! Пропущенный оператор")

    if state:
        raise errors.MissingOperandError("Ошибка! Пропущенный операнд")

def calculation(tokens: list[Token]) -> float:
    """
    Расчет результата арифметического выражения
    :param tokens: Выражение в токенах (list)
    :return: Результат (float)
    """

    # Проверяем выражение на верность
    validate(tokens)

    values = []
    operators = []

    # Рассчитываем унарные минусы для чисел и разделяем операторы и числа (лишние унарные минусы не записываем, просто домножаем число на ьultiplier)
    multiplier = 1
    for token in tokens:
        if token.type == "UNARY_MINUS":
            multiplier *= -1
        elif token.type == "NUMBER":
            values.append(token.value * multiplier)
            multiplier = 1
        else:
            operators.append(token.type)

    # составляем итоговый массив чисел (для sum())
    nums = []
    num = values[0]
    for i in range(len(operators)):
        operator = operators[i]

        # если между текущим числом a и следующим числом b стоит + или -, то просто добавляем в массив a, и принимаем за текущее число b
        if operator != "SLASH" and operator != "STAR":
            nums.append(num)
            num = values[i + 1] * ((-1) if operator == "MINUS" else 1)

        # если * или /, то выполняем эти операции над num
        else:
            if operator == "SLASH":
                if values[i + 1] == 0:
                    raise errors.DivisionByZeroError("Ошибка! Деление на ноль")
                num /= values[i + 1]
            if operator == "STAR":
                num *= values[i + 1]
    nums.append(num)

    # считаем сумму чисел - это ответ, т.к все * и / мы сделали, и все числа привели к такой форме, что между ними всеми стоит + (просто у некоторых унарный -)
    return sum(nums)

