import sqlite3
import logging
from datetime import datetime
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Состояния диалога
NAME, AGE, FAVORITE_LANGUAGE = range(3)

# Замените на ваш токен от @BotFather
BOT_TOKEN = "8218444184:AAGnzZHcwePYqWc1VlCnL5rWJa10-LXjdh4"

# Путь к базе данных
DB_PATH = "survey.db"

# Создание таблицы при старте
def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            favorite_language TEXT NOT NULL,
            completed_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    logging.info("База данных инициализирована. Таблица 'users' готова.")

# Сохранение данных пользователя
def save_to_db(user_id: int, name: str, age: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (id, name, age, favorite_language, completed_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, name, age, lang, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# /start — начало анкеты
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 👋 Добро пожаловать в анкету.\n\nКак вас зовут?"
    )
    return NAME

# Шаг 1: Имя
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if not name:
        await update.message.reply_text("Пожалуйста, введите имя.")
        return NAME
    context.user_data['name'] = name
    await update.message.reply_text("Сколько вам лет?")
    return AGE

# Шаг 2: Возраст
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.isdigit():
        await update.message.reply_text("Введите возраст цифрами.")
        return AGE
    age = int(text)
    if not (5 <= age <= 120):
        await update.message.reply_text("Укажите возраст от 5 до 120.")
        return AGE
    context.user_data['age'] = age

    keyboard = [["Python", "JavaScript"], ["Java", "C++", "Другой"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Ваш любимый язык программирования?", reply_markup=reply_markup)
    return FAVORITE_LANGUAGE

# Шаг 3: Язык программирования
async def get_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = update.message.text.strip()
    context.user_data['favorite_language'] = lang

    user_id = update.effective_user.id
    save_to_db(user_id, context.user_data['name'], context.user_data['age'], lang)

    await update.message.reply_text(
        "✅ Анкета завершена!\n\n"
        f"Имя: {context.user_data['name']}\n"
        f"Возраст: {context.user_data['age']}\n"
        f"Язык: {lang}\n\n"
        "Спасибо! Ваши данные сохранены."
    )
    return ConversationHandler.END

# Отмена
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Анкета отменена.")
    return ConversationHandler.END

# Основная функция
def main():
    init_database()  # ← гарантированное создание таблицы при запуске

    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            FAVORITE_LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_language)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_handler)
    print("✅ Анкетный бот запущен. Таблица 'users' создана (если не существовала).")
    app.run_polling()

if __name__ == "__main__":
    main()

