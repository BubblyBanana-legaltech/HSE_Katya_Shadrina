import re
import json

# === 1. Настройки ===
ICS_FILE = "calendar.ics"
OUTPUT_JSON = "court_dates.json"
CASE_NUMBER = "А40-183194/2015"

# === 2. Проверка наличия файла ===
try:
    with open(ICS_FILE, "r", encoding="utf-8") as f:
        ics_data = f.read()
except FileNotFoundError:
    print(f"❌ Файл {ICS_FILE} не найден")
    exit()

# === 3. Разделение на блоки событий ===
event_blocks = re.findall(r"BEGIN:VEVENT.*?END:VEVENT", ics_data, re.DOTALL)
print(f"🔍 Найдено {len(event_blocks)} событий для анализа")

# === 4. Парсинг событий ===
court_events = []
skipped_events = []

for block in event_blocks:
    lines = block.splitlines()
    event = {}

    for line in lines:
        if line.startswith("DTSTART"):
            event["start"] = line.strip()
        elif line.startswith("DTEND"):
            event["end"] = line.strip()
        elif line.startswith("LOCATION"):
            location = re.sub(r'LOCATION(;.*?:)?', '', line).strip()
            location = location.replace("\\,", ",").replace("\n", "")
            event["location"] = location
        elif line.startswith("DESCRIPTION"):
            event["description"] = line[11:].strip()

    # === 5. Проверка на "пустые" события ===
    reason = ""
    if "start" not in event or "end" not in event:
        reason = "Нет даты начала или окончания"
    elif "location" not in event or event["location"] == "":
        reason = "Отсутствует место проведения"
    elif CASE_NUMBER not in event.get("description", ""):
        reason = "Дело не относится к А40-183194/2015"
    elif re.search(r"VALUE=DATE:0001", event.get("start", "")) or re.search(r"VALUE=DATE:0001", event.get("end", "")):
        reason = "Дата указана как 0001-01-01 (пустое событие)"
    else:
        # === 6. Извлечение даты и времени ===
        start_match = re.search(r"(\d{8})T(\d{6})", event["start"])
        end_match = re.search(r"(\d{8})T(\d{6})", event["end"])

        if not start_match or not end_match:
            reason = "Неверный формат даты/времени"
        else:
            start_date = start_match.group(1)
            end_date = end_match.group(1)

            if start_date.startswith("0001") or end_date.startswith("0001"):
                reason = "Дата в формате 0001 (пустое событие)"
            else:
                # === 7. Форматирование даты в ISO 8601 ===
                court_events.append({
                    "case_number": CASE_NUMBER,
                    "start": f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}T{start_match.group(2)[:2]}:{start_match.group(2)[2:4]}:{start_match.group(2)[4:6]}+03:00",
                    "end": f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}T{end_match.group(2)[:2]}:{end_match.group(2)[2:4]}:{end_match.group(2)[4:6]}+03:00",
                    "location": event["location"],
                    "description": event["description"]
                })
                continue  # Переходим к следующему событию

    # === 8. Логируем "пустые" события ===
    skipped_events.append({
        "block": block,
        "reason": reason
    })

# === 9. Сохранение результата ===
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(court_events, f, ensure_ascii=False, indent=4)

# === 10. Сохранение "пустых" событий для проверки ===
with open("skipped_events.json", "w", encoding="utf-8") as f:
    json.dump(skipped_events, f, ensure_ascii=False, indent=4)

# === 11. Вывод статистики ===
print(f"✅ Найдено {len(court_events)} реальных судебных заседаний")
print(f"✅ Данные сохранены в {OUTPUT_JSON}")
print(f"ℹ️  Пропущено {len(skipped_events)} событий по следующим причинам:")
for i, event in enumerate(skipped_events[:5]):  # Выводим первые 5 пропущенных
    print(f"\n--- Событие {i + 1} ---")
    print(f"Причина: {event['reason']}")