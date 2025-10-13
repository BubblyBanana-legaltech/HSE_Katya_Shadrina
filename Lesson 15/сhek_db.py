# check_db.py
import sqlite3

conn = sqlite3.connect('survey.db')
cursor = conn.cursor()

# Убедимся, что таблица существует (на всякий случай)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        favorite_language TEXT,
        completed_at TEXT
    )
''')

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

if rows:
    print("📊 Сохранённые анкеты:")
    for row in rows:
        print(f"ID: {row[0]}, Имя: {row[1]}, Возраст: {row[2]}, Язык: {row[3]}, Дата: {row[4]}")
else:
    print("📭 Нет сохранённых анкет.")

conn.close()