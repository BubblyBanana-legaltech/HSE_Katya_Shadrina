import random
from time import perf_counter

# Шаг 1: Массив из 100 000 случайных целых чисел
array_random = [random.randint(1, 1_000_000) for _ in range(100_000)]

# Шаг 2: Массив из 100 000 словарей
dict_array = [{"num_1": random.randint(1, 1_000_000), "num_2": random.randint(1, 1_000_000)} for _ in range(100_000)]

# Шаг 3: Эффективная быстрая сортировка первого массива
start_time = perf_counter()
array_random.sort()
end_time = perf_counter()
print(f"Время сортировки первого массива: {end_time - start_time:.2f} секунд")

# Шаг 4: Сортируем второй массив по ключам 'num_1' и 'num_2'
start_time = perf_counter()
dict_array.sort(key=lambda x: (x["num_1"], x["num_2"]))
end_time = perf_counter()
print(f"Время сортировки второго массива: {end_time - start_time:.2f} секунд")

# Ограничиваем вывод небольшими фрагментами
print("\nПервые пять элементов первого массива:")
print(array_random[:5])

print("\nПервые пять элементов второго массива:")
print(dict_array[:5])