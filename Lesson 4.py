def calculate_checksum(digits, weights):
    """
    Вычисляет контрольную сумму по заданным цифрам и весовым коэффициентам.

    :param digits: Список цифр.
    :param weights: Список весовых коэффициентов.
    :return: Контрольная сумма.
    """
    return sum(digit * weight for digit, weight in zip(digits, weights))


def validate_inn_10(inn):
    """
    Проверяет корректность ИНН организации (10 знаков).

    :param inn: Строка с ИНН.
    :return: True, если ИНН корректен, иначе False.
    """
    if len(inn) != 10 or not inn.isdigit():
        return False

    # Весовые коэффициенты для ИНН организации
    weights = [2, 4, 10, 3, 5, 9, 4, 6, 8]

    # Преобразуем строку в список цифр
    digits = list(map(int, inn))

    # Вычисляем контрольную сумму
    checksum = calculate_checksum(digits[:-1], weights)

    # Вычисляем контрольное число
    control_number = checksum % 11
    if control_number > 9:
        control_number %= 10

    # Проверяем совпадение контрольного числа с последней цифрой ИНН
    return control_number == digits[-1]


def validate_inn_12(inn):
    """
    Проверяет корректность ИНН физического лица или ИП (12 знаков).

    :param inn: Строка с ИНН.
    :return: True, если ИНН корректен, иначе False.
    """
    if len(inn) != 12 or not inn.isdigit():
        return False

    # Весовые коэффициенты для первого контрольного числа
    weights_1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8]
    # Весовые коэффициенты для второго контрольного числа
    weights_2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8]

    # Преобразуем строку в список цифр
    digits = list(map(int, inn))

    # Вычисляем первую контрольную сумму
    checksum_1 = calculate_checksum(digits[:-2], weights_1)
    control_number_1 = checksum_1 % 11
    if control_number_1 > 9:
        control_number_1 %= 10

    # Вычисляем вторую контрольную сумму
    checksum_2 = calculate_checksum(digits[:-1], weights_2)
    control_number_2 = checksum_2 % 11
    if control_number_2 > 9:
        control_number_2 %= 10

    # Проверяем совпадение контрольных чисел с предпоследней и последней цифрами ИНН
    return control_number_1 == digits[-2] and control_number_2 == digits[-1]


def validate_inn(inn):
    """
    Основная функция для проверки ИНН.

    :param inn: Строка с ИНН.
    :return: True, если ИНН корректен, иначе False.
    """
    if len(inn) == 10:
        return validate_inn_10(inn)
    elif len(inn) == 12:
        return validate_inn_12(inn)
    else:
        return False


# Пример использования функции
if __name__ == "__main__":
    # Тестовые данные
    test_inns = [
        "7728268790",  # Корректный ИНН организации
        "7728268791",  # Некорректный ИНН организации
        "123456789012",  # Корректный ИНН физического лица
        "123456789013",  # Некорректный ИНН физического лица
        "12345",  # Некорректная длина
        "abcdefghij",  # Не цифры
    ]

    # Проверка каждого ИНН
    for inn in test_inns:
        print(f"ИНН: {inn}, Результат: {validate_inn(inn)}")