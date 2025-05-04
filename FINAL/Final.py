import json
import csv
import re
import os
from collections import defaultdict


# === 1. Обработка файлов traders.txt и traders.json ===
def process_traders_data():
    """Читает ИНН из traders.txt, находит данные в traders.json и сохраняет в traders.csv"""
    traders_txt_path = "traders.txt"
    traders_json_path = "traders.json"
    output_csv_path = "traders.csv"

    # Проверка наличия файлов
    if not all(os.path.exists(path) for path in [traders_txt_path, traders_json_path]):
        print("Один или несколько файлов отсутствуют!")
        return

    try:
        # Чтение ИНН из traders.txt
        with open(traders_txt_path, "r") as f:
            target_inns = [line.strip() for line in f if line.strip()]

        # Чтение данных из traders.json
        with open(traders_json_path, "r", encoding="utf-8") as f:
            traders_data = json.load(f)

        # Фильтрация данных по ИНН
        filtered_data = []
        for org in traders_data:
            if org.get("inn") in target_inns:
                filtered_data.append({
                    "inn": org["inn"],
                    "ogrn": org["ogrn"],
                    "address": org["address"]
                })

        # Сохранение в CSV
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["inn", "ogrn", "address"])
            writer.writeheader()
            writer.writerows(filtered_data)
        print(f"Данные по организациям сохранены в {output_csv_path}")

    except Exception as e:
        print(f"Ошибка при обработке traders.txt/traders.json: {e}")


# === 2. Поиск email-адресов в датасете ЕФРСБ ===
def extract_emails_from_efrsb():
    """Извлекает email-адреса из msg_text датасета ЕФРСБ и группирует по publisher_inn"""
    dataset_path = "1000_efrsb_messages.json"
    output_json_path = "emails.json"

    if not os.path.exists(dataset_path):
        print("Датасет ЕФРСБ не найден!")
        return

    def find_emails(text):
        """Поиск email-адресов через регулярное выражение"""
        pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        return re.findall(pattern, text)

    email_dict = defaultdict(set)

    try:
        with open(dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        for entry in dataset:
            publisher_inn = entry.get("publisher_inn")
            msg_text = entry.get("msg_text", "")

            if not publisher_inn or not msg_text:
                continue

            # === Безопасная обработка только валидных \uXXXX ===
            # Удаляем все escape-последовательности, кроме \uXXXX
            cleaned_text = re.sub(r'\\(?!u[0-9a-fA-F]{4})', '', msg_text)
            # Заменяем только валидные \uXXXX на символы
            decoded_text = re.sub(
                r'\\u([0-9a-fA-F]{4})',
                lambda m: chr(int(m.group(1), 16)),
                cleaned_text
            )

            # === Поиск email-адресов ===
            emails = find_emails(decoded_text)
            if emails:
                email_dict[publisher_inn].update(emails)

        result = {k: list(v) for k, v in email_dict.items()}

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Email-адреса сохранены в {output_json_path}")

    except Exception as e:
        print(f"Ошибка при обработке датасета ЕФРСБ: {e}")


# === Запуск задач ===
if __name__ == "__main__":
    print("Начало выполнения задания...")
    process_traders_data()
    extract_emails_from_efrsb()
    print("Задание завершено.")