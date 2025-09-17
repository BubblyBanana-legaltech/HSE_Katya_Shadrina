import random
from time import perf_counter

# Шаг 1: Генерируем отсортированный массив с меньшим шагом
step = random.randint(1, 3)
sorted_numbers = list(range(10, 250 * 10 ** 6 + step, step))

# Шаг 2: Генерируем 10 случайных чисел
random_numbers = [random.randint(10, len(sorted_numbers)) for _ in range(10)]
print("Случайные числа:", random_numbers)


# Шаг 3: Функция линейного поиска
def linear_search(arr, target):
    """ Линейный поиск элемента в списке """
    for i in range(len(arr)):
        if arr[i] == target:
            return True
    return False


# Шаг 4: Функция бинарного поиска
def binary_search(arr, target):
    """ Бинарный поиск элемента в отсортированном списке """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        # Элемент найден
        if arr[mid] == target:
            return True

        elif arr[mid] > target:
            right = mid - 1
        else:
            left = mid + 1

    return False


# Шаг 5: Проверка наличия чисел и замер времени
for num in random_numbers:
    start_time = perf_counter()
    found_linear = linear_search(sorted_numbers, num)
    end_time = perf_counter()
    print(
        f'Линейный поиск {num}: {"найден" if found_linear else "не найден"}, время выполнения: {(end_time - start_time) * 1000:.2f} мс')

    start_time = perf_counter()
    found_binary = binary_search(sorted_numbers, num)
    end_time = perf_counter()
    print(
        f'Бинарный поиск {num}: {"найден" if found_binary else "не найден"}, время выполнения: {(end_time - start_time) * 1000:.2f} мс\n')