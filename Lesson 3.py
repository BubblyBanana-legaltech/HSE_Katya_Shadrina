# функция вычисления факториала числа (произведение натуральных чисел от 1 до n).
# Принимает в качестве аргумента число, возвращает его факториал;
def factorial(n):
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел.")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# ●	поиск наибольшего числа из трёх. Принимает в качестве аргумента кортеж из трёх чисел, возвращает наибольшее из них
def max_of_three(numbers):
    if len(numbers) != 3:
        raise ValueError("Кортеж должен содержать ровно три числа.")
    return max(numbers)

# расчёт площади прямоугольного треугольника.
# Принимает в качестве аргумента размер двух катетов треугольника. Возвращает площадь треугольника.
def triangle_area(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Длины катетов должны быть положительными числами.")
    return 0.5 * a * b

# Пример использования функций
if __name__ == "__main__":
    # Вычисление факториала
    num = 5
    print(f"Факториал числа {num}: {factorial(num)}")

    # Поиск наибольшего числа из трёх
    numbers = (10, 25, 7)
    print(f"Наибольшее число из {numbers}: {max_of_three(numbers)}")

    # Расчёт площади прямоугольного треугольника
    a, b = 6, 8
    print(f"Площадь треугольника с катетами {a} и {b}: {triangle_area(a, b)}")

# Данные арбитражных судов (из файла)
courts_data = {
    "А33": {
        "name": "Арбитражный суд Красноярского края",
        "address": "660020, КРАЙ КРАСНОЯРСКИЙ, Г. КРАСНОЯРСК, УЛ. 7-Й КМ ЕНИСЕЙСКОГО ТРАКТА, ТЕРРИТОРИЯ ЗАО 'ТЗБ КРАЙПОТРЕБСОЮЗА'"
    },
    "А40": {
        "name": "Арбитражный суд города Москвы",
        "address": "115225, г. Москва, ул. Б. Тульская, 17"
    },
    "А56": {
        "name": "Арбитражный суд Санкт-Петербурга и Ленинградской области",
        "address": "191124, Санкт-Петербург, ул. Смольного, д. 6"
    }
}  # <-- Закрытие словаря courts_data

# Данные истца (ваши данные)
plaintiff_data = {
    "name": "Иванов Иван Иванович",
    "inn": "1234567890",
    "ogrnip": "321098765432109",
    "address": "127006, г. Москва, ул. Тверская, 1"
}

# Данные ответчиков (из файла)
respondents = [
    {
        "full_name": 'Общество с ограниченной ответственностью " ПРОДСЕРВИС "',
        "short_name": 'ООО " ПРОДСЕРВИС "',
        "inn": "2465081302",
        "ogrn": "1042402640125",
        "region": "Красноярский край",
        "category": "Обычная организация",
        "category_code": "SimpleOrganization",
        "bankruptcy_id": "12182",
        "case_number": "А33-2794/2011",
        "address": "660020, КРАЙ КРАСНОЯРСКИЙ, Г. КРАСНОЯРСК, УЛ. 7-Й КМ ЕНИСЕЙСКОГО ТРАКТА, ТЕРРИТОРИЯ ЗАО 'ТЗБ КРАЙПОТРЕБСОЮЗА'"
    },
    {
        "full_name": 'Общество с ограниченной ответственностью "ТрастИнвест"',
        "short_name": 'ООО "ТрастИнвест"',
        "inn": "7720269551",
        "ogrn": "1027720007501",
        "region": "г. Москва",
        "category": "Ликвидируемый должник",
        "category_code": "DissolvedBankruptOrganization",
        "bankruptcy_id": "60041",
        "case_number": "А40-146073/2013",
        "address": "111402, г Москва, р-н Вешняки, Жемчуговой аллея, д 5 к 2"
    }
]  # <-- Закрытие списка respondents

# Функция для генерации шапки одного документа
def generate_document_header(defendant_data, case_number):
    """
    Генерирует шапку для процессуальных документов на основе входных данных.

    :param defendant_data: Словарь с данными ответчика.
    :param case_number: Номер дела (строка).
    :return: Строка с отформатированной шапкой документа.
    """
    # Определение суда по коду из номера дела
    court_code = case_number.split("-")[0]  # Извлекаем код суда (например, "А33")
    court = courts_data.get(court_code)
    if not court:
        raise ValueError(f"Суд с кодом {court_code} не найден.")

    # Формирование шапки документа с использованием f-string
    header = (
        f"{court['name']}\n"
        f"Адрес: {court['address']}\n\n"
        f"Истец: {plaintiff_data['name']}\n"
        f"ИНН {plaintiff_data['inn']} ОГРНИП {plaintiff_data['ogrnip']}\n"
        f"Адрес: {plaintiff_data['address']}\n\n"
        f"Ответчик: {defendant_data['full_name']}\n"
        f"ИНН {defendant_data['inn']} ОГРН {defendant_data['ogrn']}\n"
        f"Адрес: {defendant_data['address']}\n\n"
        f"Номер дела {case_number}"
    )
    return header


# Функция для генерации шапок для списка ответчиков
def generate_multiple_headers(respondents_list):
    """
    Генерирует шапки для всех ответчиков из списка.

    :param respondents_list: Список словарей с данными ответчиков.
    """
    for respondent in respondents_list:
        try:
            # Вызов функции для генерации шапки
            header = generate_document_header(respondent, respondent["case_number"])
            print(header)
            print("\n" + "=" * 80 + "\n")  # Разделитель между шапками
        except ValueError as e:
            print(f"Ошибка при обработке данных: {e}")


# Пример использования функций
if __name__ == "__main__":
    # Генерация шапок для всех ответчиков
    generate_multiple_headers(respondents)


